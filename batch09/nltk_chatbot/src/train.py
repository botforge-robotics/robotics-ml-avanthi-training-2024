#!/usr/bin/env python3
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import rospkg
import os

stemmer = LancasterStemmer()
rospack = rospkg.RosPack()

# load intents
intents_json_path = os.path.join(rospack.get_path(
    'nltk_chatbot'),  'dataset/intents/intents.json')
with open(intents_json_path) as file:
    data = json.load(file)

try:
    intents_pickle_path = os.path.join(rospack.get_path(
        'nltk_chatbot'),  'dataset/intents/intents_data.pickle')
    with open(intents_pickle_path, "rb") as file:
        words, labels, training, output = pickle.load(
        file)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open(intents_pickle_path, "wb") as f:
        pickle.dump((words, labels, training, output), f)


tensorflow.compat.v1.reset_default_graph()
# define deep neural network layers
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(net, 16)
net = tflearn.fully_connected(
    net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

# load trained model to network
model = tflearn.DNN(net)

model.fit(training, output, n_epoch=300, batch_size=8, show_metric=True)
model_path = os.path.join(rospack.get_path(
    'nltk_chatbot'),  'dataset/model/model.tflearn')
model.save(model_path)