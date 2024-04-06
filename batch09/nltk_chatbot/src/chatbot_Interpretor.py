#!/usr/bin/env python3.7

import rospy
import os
from nltk_chatbot_msg.srv import TextService ,TextServiceResponse
from nltk_chatbot_msg.srv import VoiceService, VoiceServiceResponse
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import time
import rospkg
from std_msgs.msg import String
from std_msgs.msg import Float32
from std_srvs.srv import SetBool,SetBoolRequest
from face_recognition.srv import RecognisePersonsOnce, RecognisePersonsOnceRequest
rospack = rospkg.RosPack()
stemmer = LancasterStemmer()

temperature =0.0
humidity = 0.0

# text service
def text_service_callback(req):
    res = TextServiceResponse()
    intent_tag_msg = String()
    if not req.query_text == "none":
        res.response_text,intent_tag_msg.data = interpret(req.query_text)
    else:
        res.response_text ="can't understand"
        intent_tag_msg.data= "none"
    intent_tag_pub.publish(intent_tag_msg)
    return res

# voice service
def voice_service_callback(req):
    res= VoiceServiceResponse()
    intent_tag_msg = String()
    if not req.query_text == "none":
        processed_string,intent_tag_msg.data = interpret(req.query_text)
        text_to_speech_msg = String()
        if intent_tag_msg.data == "temperature":
            text_to_speech_msg.data = processed_string.replace("value", "{:.2f}".format(temperature))
        elif intent_tag_msg.data == "humidity":
            text_to_speech_msg.data = processed_string.replace("value", "{:.2f}".format(humidity))
        elif intent_tag_msg.data == "greeting" or intent_tag_msg.data == "farewell":
            response = recognise_face_client(RecognisePersonsOnceRequest())
            if(response.success):
                text_to_speech_msg.data = processed_string.replace("value", response.persons[0])
            else:
                text_to_speech_msg.data = processed_string.replace("value", "")
        elif intent_tag_msg.data == "guess_me":
            response = recognise_face_client(RecognisePersonsOnceRequest())
            if(response.success):
                text_to_speech_msg.data = processed_string.replace("value", response.persons[0])
            else:
                text_to_speech_msg.data = "sory i cant recognise you"
        elif intent_tag_msg.data == "object_detection":
            request = SetBoolRequest()
            request.data = True
            response = object_detection_service_client(request)
            if(response.success):
                text_to_speech_msg.data = processed_string + response.message
            else:
                text_to_speech_msg.data = "Sorry I am unable to find anything."
        else:
            text_to_speech_msg.data = processed_string 
        intent_tag_pub.publish(intent_tag_msg)
        text_to_speech_pub.publish(text_to_speech_msg)
        # Set the response to be True
        res.success = True
    else:
        intent_tag_msg.data= "none"
        res.success = False
        intent_tag_pub.publish(intent_tag_msg)
    return res

#  interpretor
def interpret(query):
    results = model.predict([bag_of_words(query, words)])
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    responses = None
    for tg in data["intents"]:
        if tg["tag"] == tag:
            responses = tg['responses']
    return (random.choice(responses),tag)

# expands words
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)
 

rospy.init_node('chatbot_interpreter_node')

def temperature_callback(msg):
    global temperature
    temperature = msg.data
def humidity_callback(msg):
    global humidity
    humidity = msg.data
# Create the service servers
srv_string_to_string = rospy.Service(
     'chatbot_interpreter_node/text_service',TextService, text_service_callback)
srv_string_to_speech = rospy.Service(
     'chatbot_interpreter_node/voice_service',VoiceService, voice_service_callback)

object_detection_service_client = rospy.ServiceProxy("/detect_objects",SetBool)

recognise_face_client = rospy.ServiceProxy("/recognise_persons_once",RecognisePersonsOnce)

intent_tag_pub = rospy.Publisher('chatbot_intent_tag',String, queue_size=2)
text_to_speech_pub = rospy.Publisher('text_to_say',String, queue_size=2)

rospy.Subscriber("temperature",Float32, temperature_callback, queue_size=3)
rospy.Subscriber("humidity",Float32, humidity_callback, queue_size=3)

# load intents
intents_json_path = os.path.join(rospack.get_path(
    'nltk_chatbot'),  'dataset/intents/intents.json')
with open(intents_json_path) as file:
    data = json.load(file)

intents_pickle_path = os.path.join(rospack.get_path(
    'nltk_chatbot'),  'dataset/intents/intents_data.pickle')
with open(intents_pickle_path, "rb") as file:
    words, labels, training, output = pickle.load(
        file)

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
model_path = os.path.join(rospack.get_path(
    'nltk_chatbot'),  'dataset/model/model.tflearn')
model.load(model_path)

rospy.loginfo("chatbot interpretor ready!!")
rospy.spin()

    

   


