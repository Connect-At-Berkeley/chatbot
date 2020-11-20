import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle

import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random

words=[]
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('intents.json').read()
intents = json.loads(data_file)

### JSON DATA in intents.json
# {"intents": [
#         {"tag": "greeting",
#          "patterns": ["Hi there", "How are you", "Is anyone there?","Hey","Hola", "Hello", "Good day"],
#          "responses": ["Hello, thanks for asking", "Good to see you again", "Hi there, how can I help?"],
#          "context": [""]
#         },
#         .
#         .
#         .
#         {"tag": "search_hospital_by_type",
#         "patterns": [],
#         "responses": ["Loading hospital details"],
#         "context": [""]
#         }
#     ]
# }

for intent in intents['intents']:
    for pattern in intent['patterns']:

        # take each word and tokenize it
        w = nltk.word_tokenize(pattern)
        # adds to list of words
        words.extend(w)
        # adding documents
        documents.append((w, intent['tag']))

        # adding classes to our class list
        print("TAG: ", intent['tag'])
        if intent['tag'] not in classes:

            classes.append(intent['tag'])

# gets all the words from all patterns and puts them into "words" list
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# all the tags from intents.json is stored in classes (as long as the tags have at least one pattern)
classes = sorted(list(set(classes)))

print (len(documents), "documents")
print (len(classes), "classes", classes)
print (len(words), "unique lemmatized words", words)


pickle.dump(words, open('words.pkl','wb'))
pickle.dump(classes, open('classes.pkl','wb'))

# initializing training data
training = []
output_empty = [0] * len(classes)

# verbose stuff
# print("WORDS: ", words)
# print("DOCUMENTS: ", documents)
# print("CLASSES: ", classes)

for doc in documents:
    # initializing bag of words
    bag = []
    # assigns pattern_words to a list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    print("PATTERN_WORDS: ", pattern_words);
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    print("OUTPUT_ROW: ", output_row)
    print([bag, output_row]);

    # adds the bag of words (array of 0s or 1s) and output_row which is the tags (in array format with 0s and 1s)
    training.append([bag, output_row])
# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")


# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

#fitting and saving the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)

print("model created")




lemmatizer = WordNetLemmatizer()
model = load_model('chatbot_model.h5')
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    print("clean_up_sentence")
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    print("bow")
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    print("predict_class")
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

#def getResponse(ints, intents_json):
#    print("getResponse")
#    tag = ints[0]['intent']
#    list_of_intents = intents_json['intents']
#    for i in list_of_intents:
#        if(i['tag']== tag):
#            result = random.choice(i['responses'])
#            break
#    return result

def chatbot_response(msg):
    print("chatbot_response")
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

def links(ints, intents_json):
    print("link")
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = i['links']
            break
    return result
def getResponse(ints, intents_json):
    print("getResponse")
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            resources = i['responses']
            break
    links = links(ints, intents_json)
    result = []
    count = 0
    for i in range(len(resources)):
        if i % 2 == 0:
            result[i] = resources[count]
        else:
            result[i] = links[count]
            count += 1
    return result


# create function that gets links

####### CHATTERBOT API STUFF #######
# from chatterbot import ChatBot
#
# import nltk
# import ssl
#
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download()
#
# chatbot = ChatBot(
#     'CoronaBot',
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     logic_adapters=[
#         'chatterbot.logic.MathematicalEvaluation',
#         'chatterbot.logic.TimeLogicAdapter',
#         'chatterbot.logic.BestMatch',
#         {
#             'import_path': 'chatterbot.logic.BestMatch',
#             'default_response': 'I am sorry, but I do not understand. I am still learning.',
#             'maximum_similarity_threshold': 0.90
#         }
#     ],
#     database_uri='sqlite:///database.sqlite3'
# )
#
# # Training With Own Questions
# from chatterbot.trainers import ListTrainer
#
# trainer = ListTrainer(chatbot)
#
# training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
# training_data_personal = open('training_data/personal_ques.txt').read().splitlines()
#
# training_data = training_data_quesans + training_data_personal
#
# trainer.train(training_data)
#
# # Training With Corpus
# from chatterbot.trainers import ChatterBotCorpusTrainer
#
# trainer_corpus = ChatterBotCorpusTrainer(chatbot)
#
# trainer_corpus.train(
#     'chatterbot.corpus.english'
# )
