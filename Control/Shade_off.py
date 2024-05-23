import RPi.GPIO as GPIO
from datetime import datetime, time
import time as t

channel_16 = 16 #change channel_16 based on relay

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(channel_16, GPIO.OUT)

def shade_ret_off(pin):
    GPIO.output(pin, GPIO.HIGH)  

def shade_ret_on(pin):
    GPIO.output(pin, GPIO.LOW)  

try:
    while True:
            shade_ret_on(channel_16)
            t.sleep(5)
            shade_ret_off(channel_16)
            t.sleep(5)


except KeyboardInterrupt:
    GPIO.cleanup()
