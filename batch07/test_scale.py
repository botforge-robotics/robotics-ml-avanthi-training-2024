#!/usr/bin/env python3

import RPi.GPIO as GPIO 
from hx711 import HX711
import time

c_value = 0
ratio = 438.75035340684195
def find_weight():
    global c_value
    global hx
    if c_value == 0:
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
    else :
          GPIO.setmode(GPIO.BCM)
          time.sleep(1)
          try:
                weight = int(hx.get_weight_mean(20))
                #round(weight,1)
                print(weight, 'g')
                return weight
          except (KeyboardInterrupt, SystemExit):
                print('Bye :)')

while True:
    find_weight()