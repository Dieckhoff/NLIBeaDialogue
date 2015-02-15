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

# other global variables:
allPhrases = [prepositionalPhrase, nominalPhrase, adjectivePhrase, verbalPhrase, sentence]
allTerminals = [noun, verb, preposition, conjunction, determiner, adjective, adverb, pronoun, properNoun]
globalStateSet = []

def earley(words):
  chart = []
  initialState = State()
  initialState.rule = {"start": "$", "end": "@S"}
  initialState.index = [0, 0]
  addtochart(initialState, 0)
  for i, word in enumerate(words):
    for j, state in enumerate(globalStateSet[i]):
      if ("@" in state.rule["end"]) and not isTerminal(afterDot(state.rule["end"])) and not afterDot(state.rule["end"]) == "":
        print "predicting: ", state.rule["start"], "-->", state.rule["end"]
        predictor(state)
      elif ("@" in state.rule["end"]) and isTerminal(state.rule["end"]):
        print "scanning: ", state.rule["start"], "-->", state.rule["end"]
        scanner(state, word)
      else:
        print "completing: ", state.rule["start"], "-->", state.rule["end"]
        completer(state) # dot is at the end of rule's right hand side
  printChart()

def predictor(state):
  predicted = afterDot(state.rule["end"])
  print "predicted: ", predicted
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
  scannedTerminal = [terminal for terminal in allTerminals if terminal.abbreviation == scanned]
  if word in scannedTerminal:
    newState = State()
    newState.rule = {"start": scanned, "end": (word, "@")}
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
    before = state.rule["end"].split("@")[0]
    after = state.rule["end"].split("@")[-1][1:]
    x = after.split( )
    x.insert(1, "@")
    newAfter = "".join(x)
    newEnd = "".join([before, newAfter])
    # adding new state to chart:
    newState = State()
    newState.rule = {"start": state.rule["start"], "end": newEnd}
    newState.index = [state.index[0], k]
    addtochart(newState, k)
    # print "shifting. before: ", before, " after: ", after, " newAfter: ", newAfter, " newEnd: ", newEnd

def addtochart(state, index):
  if len(globalStateSet) <= index:
    globalStateSet.append([state])
  elif state not in globalStateSet[index]:
    globalStateSet[-1].append(state)

def incomplete(state):
  return (afterDot(state.rule["end"]) != "") # True if there is a symbol after the dot

def afterDot(state):
  # @ symbolizes the dot
  # print "in afterdot function. ", state
  x = state.split("@")[-1]
  if x != "":
    y = x.split( )[0]
    if y != "@":
      return y # return the first symbol after the dot
  else:
    return ""

def isTerminal(symbol):
  return (symbol in [t.abbreviation for t in allTerminals])

def printChart():
  print globalStateSet

inputSentence = "I am Bea"
inputSentenceAsList = inputSentence.split( )
earley(inputSentenceAsList)

# # preparation:
# inputSentence = "I am Bea"
# inputAsList = inputSentence.split( )
# output = earley(inputAsList)
# finalStartRule = {"start": "R", "end": "S"}
# if finalStartRule in output[-1]:
#   i = output.index(finalStartRule)
#   j = 0
#   b = [finalStartRule]
#   recursion(i, j, b, output)
# else:
#   print "Syntax Error!"

# def parseText(inputAsList):
#   emptyStateSet = [finalStartRule]
#   for word, i in inputAsList:
#     newState = State(i+1)
#     emptyStateSet.append(newState)
#     possibleStateSet = addEarleyStates(emptyStateSet)
#   return possibleStateSet

# def recursion(i, j, b, stateSet):
#   # i: Index of current state set Qi
#   # j: Index of current state bj in tree b
#   while j > 0:
#     # backwards-predictor:


# def predict(tree, word):
#   print "This is about: ", word
#   print "state: ", tree.branches.last().name
#   if hasattr(tree, "rules"):
#     for rule in tree.rules:
#       for el in rule:
#         if predict(el, word) == True:
#           return True
#         else: predict(el, word)
#   elif hasattr(tree, "elements"):
#     return scan(tree, word)
#   else: print "tree without elements..."

# def scan(partOfSpeech, word):
#   print "scanning: ", word, " in: ", partOfSpeech.name
#   return (word in partOfSpeech.elements)

# # def complete():
# #   return
