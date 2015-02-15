import pdb

# classes:
class PartOfSpeech(object):
  name = ""
  abbreviation = ""
  elements = []

class Phrase(object):
  name = ""
  abbreviation = ""
  rules = []

class State(object):
  rule = {}
  index = []

class TreeChart(object):
  branches = []

# Parts of Speech - Initialization of words:
noun = PartOfSpeech()
noun.name = "noun"
noun.abbreviation = "N"
noun.elements = ["enrolment", "fee", "subject", "help", "issue", "information"]

properNoun = PartOfSpeech()
properNoun.name = "proper noun"
properNoun.abbreviation = "PN"
properNoun.elements = ["www.upf.edu", "Bea"]

verb = PartOfSpeech()
verb.name = "verb"
verb.abbreviation = "V"
verb.elements = ["can", "pay", "am", "need", "read"]

pronoun = PartOfSpeech()
pronoun.name = "pronoun"
pronoun.abbreviation = "P"
pronoun.elements = ["I", "you"]

determiner = PartOfSpeech()
determiner.name = "determiner"
determiner.abbreviation = "DET"
determiner.elements = ["the", "that", "this"]

adjective = PartOfSpeech()
adjective.name = "adjective"
adjective.abbreviation = "ADJ"
adjective.elements = ["familiar"]

adverb = PartOfSpeech()
adverb.name = "adverb"
adverb.abbreviation = "ADV"
adverb.elements = ["further", "not", "then"]

conjunction = PartOfSpeech()
conjunction.name = "conjunction"
conjunction.abbreviation = "C"
conjunction.elements = ["if"]

preposition = PartOfSpeech()
preposition.name = "preposition"
preposition.abbreviation = "PREP"
preposition.elements = ["with", "about", "on"]

# Phrases - Initialization of rules:
prepositionalPhrase = Phrase()
nominalPhrase = Phrase()
adjectivePhrase = Phrase()
verbalPhrase = Phrase()
sentence = Phrase()

prepositionalPhrase.name = "prepositional phrase"
prepositionalPhrase.abbreviation = "PP"
prepositionalPhrase.rules = ["PREP NP"]

nominalPhrase.name = "nominal phrase"
nominalPhrase.abbreviation = "NP"
nominalPhrase.rules = ["DET N", "DET NP", "N NP", "N", "ADV NP", "P", "PN"]

adjectivePhrase.name = "adjective phrase"
adjectivePhrase.abbreviation = "ADJP"
adjectivePhrase.rules = ["ADJP PP", "ADV ADJP", "ADJ", "ADV"]

verbalPhrase.name = "verbal phrase"
verbalPhrase.abbreviation = "VP"
verbalPhrase.rules = ["P VP", "V VP", "V", "VP ADJP", "C VP"]

sentence.name = "sentence"
sentence.abbreviation = "S"
sentence.rules = ["VP NP", "S S"]

# sentence.rules = ["NP VP"]
# nominalPhrase.rules = ["P"]
# verbalPhrase.rules = ["V PN"]

# other global variables:
allPhrases = [prepositionalPhrase, nominalPhrase, adjectivePhrase, verbalPhrase, sentence]
allTerminals = [noun, verb, preposition, conjunction, determiner, adjective, adverb, pronoun, properNoun]
globalStateSet = []
placeholderstate = State()
placeholderstate.rule = {"start": "*", "end": "@*"}
placeholderstate.index = [0, 0]

def earley(words):
  chart = []
  initialState = State()
  initialState.rule = {"start": "$", "end": "@S"}
  initialState.index = [0, 0]
  addtochart(initialState, 0)
  for i, word in enumerate(words):
    if len(globalStateSet) <= i:
      addtochart(placeholderstate, i)
    for j, state in enumerate(globalStateSet[i]):
      # print "state rule: ", state.rule["start"], "-->", state.rule["end"], i, word, j
      if not isTerminal(afterDot(state.rule["end"])) and not afterDot(state.rule["end"]) == "":
        print "predicting: ", state.rule["start"], "-->", state.rule["end"]
        predictor(state)
      elif isTerminal(afterDot(state.rule["end"])):
        print "scanning: ", state.rule["start"], "-->", state.rule["end"]
        scanner(state, word)
      else:
        print "completing: ", state.rule["start"], "-->", state.rule["end"]
        completer(state) # dot is at the end of rule's right hand side
  printChart()

def predictor(state):
  predicted = afterDot(state.rule["end"])
  predictedPhrase = [phrase for phrase in allPhrases if phrase.abbreviation == predicted][0]
  currentChartIndex = state.index[-1] # second index
  for end in predictedPhrase.rules:
    newState = State()
    newState.rule = {"start": predicted, "end": "".join(["@", end])}
    newState.index = [currentChartIndex, currentChartIndex]
    addtochart(newState, currentChartIndex)

def scanner(state, word):
  currentSentenceIndex = state.index[-1] # second index
  scanned = afterDot(state.rule["end"])
  scannedTerminal = [terminal for terminal in allTerminals if terminal.abbreviation == scanned][0]
  if word in scannedTerminal.elements:
    print word, " is a ", scannedTerminal.name, "\n"
    newState = State()
    newState.rule = {"start": scanned, "end": "".join([word, "@"])}
    newState.index = [currentSentenceIndex, currentSentenceIndex+1]
    addtochart(newState, currentSentenceIndex+1)

def completer(state):
  start = state.rule["start"]
  end = state.rule["end"]
  j = state.index[0]
  k = state.index[-1]
  currentChartPart = globalStateSet[j]
  relevantStates = [state for state in currentChartPart if (state.index[-1] == j) and (afterDot(state.rule["end"]) == start)]
  for state in relevantStates:
    # shifting the dot one further:
    splitted = state.rule["end"].split("@")
    before = splitted[0]
    after = splitted[-1]
    x = after.split( )
    x.insert(1, "@")
    newAfter = "".join(x)
    newEnd = "".join([before, newAfter])
    # adding new state to chart:
    newState = State()
    newState.rule = {"start": state.rule["start"], "end": newEnd}
    newState.index = [state.index[0], k]
    addtochart(newState, k)

def addtochart(state, index):
  if len(globalStateSet) <= index:
    globalStateSet.append([state])
  elif globalStateSet[index] == [placeholderstate]:
    globalStateSet[index] = [state]
  elif state not in globalStateSet[index]:
    globalStateSet[-1].append(state)

def incomplete(state):
  return (afterDot(state.rule["end"]) != "") # True if there is a symbol after the dot

def afterDot(state):
  # @ symbolizes the dot
  x = state.split("@")[-1]
  if x != "":
    y = x.split( )[0]
    if y != "@":
      return y # return the first symbol after the dot
    else:
      return ""
  else:
    return ""

def isTerminal(symbol):
  x = (symbol in [t.abbreviation for t in allTerminals])
  return x

def printChart():
  print "\nHere is the chart:\n_____________________\n"
  for x in globalStateSet:
    for y in x:
      print y.index, " ", y.rule["start"], " --> ", y.rule["end"]

inputSentence = "Then you can pay the enrolment fee"
inputSentenceAsList = inputSentence.split( )
earley(inputSentenceAsList)