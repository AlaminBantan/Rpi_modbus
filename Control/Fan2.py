import RPi.GPIO as GPIO
from datetime import datetime, time
import time as t

channel_20 = 20 #change channel_20 based on relay

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(channel_20, GPIO.OUT)

def fan2_off(pin):
    GPIO.output(pin, GPIO.HIGH)  

def fan2_on(pin):
    GPIO.output(pin, GPIO.LOW)  

try:
    while True:
      
        # Get the current time
        current_time = datetime.now().time()

        # Define the start and end times
        start_time_f2 = time(6, 0, 40)
        morning_time_f2 = time(9,59,40)
        end_time_f2 = time(18, 0)

        # Check if the current time is between 6:00:45 AM and 6:00 PM
        if start_time_f2 <= current_time <= morning_time_f2:
            print("The current time is between 6:00 AM and 10:00 PM.")
            print("fan2 is on")
            fan2_on(channel_20)
            t.sleep(1140)
            print("fan is off")
            fan2_off(channel_20)
            t.sleep(60)
        elif morning_time_f2 <= current_time <= end_time_f2:
            print("The current time is between 10:00 AM and 6:00 PM.")
            print("fan is off")
            fan2_off(channel_20)
            t.sleep(60)
            print("fan is on")
            fan2_on(channel_20)
            t.sleep(1740)

        else:
            print("its night time, go and rest")
            fan2_off(channel_20)
            t.sleep(1)


except KeyboardInterrupt:
    GPIO.cleanup()
