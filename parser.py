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

# Parts of Speech - Initialization of words:
noun = PartOfSpeech()
noun.name = "noun"
noun.abbreviation = "N"
noun.elements = ["enrolment", "fee", "subject", "help", "issue", "information"]

properNoun = PartOfSpeech()
properNoun.name = "proper noun"
properNoun.abbreviation = "PN"
properNoun.elements = ["www.upf.edu", "Anita"]

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
adjectivePhrase.rules = [[adjectivePhrase, prepositionanlPhrase], [adverb, adjectivePhrase], [adjective], [adverb]]

verbalPhrase.name = "verbal phrase"
verbalPhrase.abbreviation = "VP"
verbalPhrase.rules = [[pronoun, verbalPhrase], [verb, verbalPhrase], [verb], [verbalPhrase, adjectivePhrase], [conjunction, verbalPhrase]]

sentence.name = "sentence"
sentence.abbreviation = "S"
sentence.rules = [[verbalPhrase, nominalPhrase], [sentence, sentence]]

# root = [[sentence]]

def earley(inputSentence):
  inputList = inputSentence.split( )
  for word in inputList:
    predict(root, word)

def predict(state, word):
  print "This is about: ", word
  for option in state:
    if type(option) != str:
      for tag, tagList in option.iteritems():
        if predict(tagList, word) == True:
          break
    elif scan(state, word) == True:
      print "true! The word ", word, " is a: ", state
      return True
    else: return "not correct"

def scan(partOfSpeech, word):
  print "scanning"
  return (word in partOfSpeech)

# def complete():
#   return

earley("I am Anita")
