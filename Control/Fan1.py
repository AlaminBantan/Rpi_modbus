import RPi.GPIO as GPIO
from datetime import datetime, time
import time as t

channel_fan1 = 21 #change channel_21 based on relay

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(channel_fan1, GPIO.OUT)

def fan1_off(pin):
    GPIO.output(pin, GPIO.HIGH)  

def fan1_on(pin):
    GPIO.output(pin, GPIO.LOW)  

try:
    while True:
      
        # Get the current time
        current_time = datetime.now().time()


        if (time(6, 0) <= current_time <= time(7, 59, 49)) or ((time(16, 0) <= current_time <= time(18,0))):
            print("no misting right now, fans are on")
            fan1_on(channel_fan1)
        elif (time(7,59,50) <= current_time <= time(16,0)):
            print("misting right now, fans are off")
            fan1_off(channel_fan1)
            t.sleep(30)
            print("no misting right now, fans are on")
            fan1_on(channel_fan1)
            t.sleep(1410)
        else:
            print("its night time, go and sleep")
            fan1_off(channel_fan1)


except KeyboardInterrupt:
    GPIO.cleanup()
