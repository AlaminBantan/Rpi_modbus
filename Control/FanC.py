import RPi.GPIO as GPIO
from datetime import datetime, time
import time as t

channel = 2 #change channel based on relay

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(channel, GPIO.OUT)

def fan_c_off(pin):
    GPIO.output(pin, GPIO.HIGH)  

def fan_c_on(pin):
    GPIO.output(pin, GPIO.LOW)  

try:
    while True:
      
        # Get the current time
        current_time = datetime.now().time()

        # Define the start and end times
        start_time_fan_c = time(6, 00)
        end_time_fan_c = time(18, 00)

        # Check if the current time is between 6:00 AM and 6:00 PM:
        if start_time_fan_c <= current_time <= end_time_fan_c:
            print("The current time is between 6 AM and 6 PM")
            print("Fan in zone C is on now")
            fan_c_on(channel)
            t.sleep(180)
        else:
            print("no change to shading now")
            fan_c_off(channel)
            t.sleep(1)


except KeyboardInterrupt:
    GPIO.cleanup()
