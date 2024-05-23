import RPi.GPIO as GPIO
from datetime import datetime, time
import time as t

channel_19 = 19 #change channel_19 based on relay

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(channel_19, GPIO.OUT)

def shade_ex_off(pin):
    GPIO.output(pin, GPIO.HIGH)  

def shade_ex_on(pin):
    GPIO.output(pin, GPIO.LOW)  

try:
    while True:
      
        # Get the current time
        current_time = datetime.now().time()

        # Define the start and end times
        start_time_shade_ex = time(10, 30)
        end_time_shade_ex = time(10, 33)

        # Check if the current time is between 10:30 AM and 10:33 AM:
        if start_time_shade_ex <= current_time <= end_time_shade_ex:
            print("The current time is 10:30, shades will be extended now")
            print("shade is expanding now")
            shade_ex_on(channel_19)
            t.sleep(180)
        else:
            print("no change to shading now")
            shade_ex_off(channel_19)
            t.sleep(1)


except KeyboardInterrupt:
    GPIO.cleanup()
