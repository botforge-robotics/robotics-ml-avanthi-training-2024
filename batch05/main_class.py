#!/usr/bin/env python3.8

import RPi.GPIO as GPIO 
from hx711 import HX711
import time
import board
import neopixel
from datetime import datetime
import requests
import json
from requests.structures import CaseInsensitiveDict
import cv2
import sys
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

import signal

pixels = neopixel.NeoPixel(board.D12, 44, brightness=1)
c_value = 0
ratio = 438.75035340684195
weightThreshold =3
flag = False

base_options = core.BaseOptions(
        file_name="model/model.tflite", use_coral=False, num_threads=4)

# Enable Coral by this setting
classification_options = processor.ClassificationOptions(
    max_results=1, score_threshold=0.5)
options = vision.ImageClassifierOptions(
    base_options=base_options, classification_options=classification_options)

classifier = vision.ImageClassifier.create_from_options(options)

class_names = [
    "RealOrange_1L",
    "LaysTomato_50G",
    "Bourbon_100G",
    "KurkureChilli_36G"
]
prices={
    "RealOrange_1L":130,
    "LaysTomato_50G":20,
    "Bourbon_100G":25,
    "KurkureChilli_36G":10
}
def signal_handler(sig, frame):
    print("Ctrl+C detected. Exiting gracefully.")
    # cap.release()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
def callibrateScale():
    global c_value
    global hx
    print('Calibration starts')
    try:
        GPIO.setmode(GPIO.BCM)
        hx = HX711(dout_pin=20, pd_sck_pin=21)
        err = hx.zero()
        if err:
            raise ValueError('Tare is unsuccessful.')
        hx.set_scale_ratio(ratio)
        c_value = 1
    except (KeyboardInterrupt, SystemExit):
        print('Bye :)')
    print('Calibrate ends')
    

def find_weight():
    global hx
    GPIO.setmode(GPIO.BCM)
    time.sleep(0.2)
    try:
        weight = int(hx.get_weight_mean(6))
        #round(weight,1)
        return weight
    except (KeyboardInterrupt, SystemExit):
        print('Bye :)')

def post(id_product,label,price,final_rate,taken):
    url = "http://localhost:3000/product"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    data_dict = {"id":id_product,"name":label,"price":price,"unit":"Nos","taken":taken,"payable":final_rate}
    data = json.dumps(data_dict)
    resp = requests.post(url, headers=headers, data=data)
    print(resp.status_code)

# turn red color led
pixels.fill((255, 0, 0))
# start callibration
callibrateScale()
# turn orange led
pixels.fill((242, 119, 26))
time.sleep(0.12)
while True:
    # check if weight has increased
    if(find_weight() > weightThreshold and not flag):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        flag= True
        # turn led red color -processing
        pixels.fill((255, 0, 0))
        ret, frame = cap.read()
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite("sample.jpg",frame)
        cap.release()
        # Create TensorImage from the RGB image
        tensor_image = vision.TensorImage.create_from_array(rgb_image)
        # List classification results
        categories = classifier.classify(tensor_image)
        # Print classification results
        if len(categories.classifications[0].categories)>0:
            class_idx = categories.classifications[0].categories[0].index
            print(categories)
            print(categories.classifications[0].categories[0].index)
            post(class_idx,class_names[class_idx].split("_")[0],prices[class_names[class_idx]],prices[class_names[class_idx]],1)
        pixels.fill((0, 255, 0))
    elif (flag and find_weight() <= weightThreshold):
        flag = False
        pixels.fill((242, 119, 26))

pixels.fill((0, 0, 0))