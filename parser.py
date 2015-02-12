import pdb

# words:
nouns = ["enrolment", "fee", "subject", "help", "issue", "information"]
properNouns = ["www.upf.edu", "Anita"]
verbs = ["can", "pay", "am", "need", "read"]
pronouns = ["I", "you"]
determiners = ["the", "that", "this"]
adjectives = ["familiar"]
adverbs = ["further", "not", "then"]
conjunctions = ["if"]
prepositions = ["with", "about", "on"]

# initialization:
prepositionanlPhrase = []
nominalPhrase = []
adjectivePhrase = []
verbalPhrase = []
sentence = []

# rules:
prepositionanlPhrase = [{"prep": prepositions, "NP": nominalPhrase}]
nominalPhrase = [{"DET": determiners, "N": nouns}, {"DET": determiners, "NP": nominalPhrase}, {"N": nouns, "NP": nominalPhrase}, {"N": nouns}, {"ADV": adverbs, "NP": nominalPhrase}, {"P": pronouns}, {"PN": properNouns}]
adjectivePhrase = [{"ADJP": adjectivePhrase, "PP": prepositionanlPhrase}, {"ADV": adverbs, "ADJP": adjectivePhrase}, {"ADJ": adjectives}, {"ADV": adverbs}]
verbalPhrase = [{"P": pronouns, "VP": verbalPhrase}, {"V": verbs, "VP": verbalPhrase}, {"V": verbs}, {"VP": verbalPhrase, "ADJP": adjectivePhrase}, {"C": conjunctions, "VP": verbalPhrase}]
sentence = [{"VP": verbalPhrase, "NP": nominalPhrase}, {"S": sentence, "S": sentence}]
root = [{"S": sentence}]

def earley(inputSentence):
  # tree = sentence
  inputList = inputSentence.split( )
  for word in inputList:
    # pdb.set_trace()
    print predict(root, word)

def predict(state, word):
  print "This is about: ", word
  # pdb.set_trace()
  for option in state:
    # pdb.set_trace()
    # print option
    if type(option) != str:
      # pdb.set_trace()
      for tag, tagList in option.iteritems():
        # pdb.set_trace()
        print tag
        if predict(tagList, word) == True:
          break
    elif scan(state, word) == True:
      # pdb.set_trace()
      print "true! The word ", word, " is a: ", state
      return True
    else: return "not correct"

def scan(partOfSpeech, word):
  print "scanning"
  return (word in partOfSpeech)

# def complete():
#   return

earley("I am Anita")
