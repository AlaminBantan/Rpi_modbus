import RPi.GPIO as GPIO
from datetime import datetime, time
import time as t

channel_23 = 23 #change channel_23 based on relay

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(channel_23, GPIO.OUT)

def mist_off(pin):
    GPIO.output(pin, GPIO.HIGH)  

def mist_on(pin):
    GPIO.output(pin, GPIO.LOW)  

try:
    while True:
            mist_on(channel_23)
            t.sleep(10)
            mist_off(channel_23)
            t.sleep(10)



except KeyboardInterrupt:
    GPIO.cleanup()
