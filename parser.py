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

class State(object, i):
  index = i
  rule = {"start": "", "end": ""}
  word = ""

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
prepositionalPhrase.rules = [[preposition, nominalPhrase]]

nominalPhrase.name = "nominal phrase"
nominalPhrase.abbreviation = "NP"
nominalPhrase.rules = [[determiner, noun], [determiner, nominalPhrase], [noun, nominalPhrase], [noun], [adverb, nominalPhrase], [pronoun], [properNoun]]

adjectivePhrase.name = "adjective phrase"
adjectivePhrase.abbreviation = "ADJP"
adjectivePhrase.rules = [[adjectivePhrase, prepositionalPhrase], [adverb, adjectivePhrase], [adjective], [adverb]]

verbalPhrase.name = "verbal phrase"
verbalPhrase.abbreviation = "VP"
verbalPhrase.rules = [[pronoun, verbalPhrase], [verb, verbalPhrase], [verb], [verbalPhrase, adjectivePhrase], [conjunction, verbalPhrase]]

sentence.name = "sentence"
sentence.abbreviation = "S"
sentence.rules = [[verbalPhrase, nominalPhrase], [sentence, sentence]]

# preparation:
inputSentence = "I am Bea"
inputAsList = inputSentence.split( )
output = earley(inputAsList)
finalStartRule = {"start": "R", "end": "S"}
if finalStartRule in output[-1]:
  i = output.index(finalStartRule)
  j = 0
  b = [finalStartRule]
  recursion(i, j, b, output)
else:
  print "Syntax Error!"

def parseText(inputAsList):
  emptyStateSet = [finalStartRule]
  for word, i in inputAsList:
    newState = State(i+1)
    emptyStateSet.append(newState)
    possibleStateSet = addEarleyStates(emptyStateSet)
  return possibleStateSet

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
