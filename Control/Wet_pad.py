import RPi.GPIO as GPIO
from datetime import datetime, time
import threading
import time as t

# Define GPIO channels
channel_pump = 14 #connect the wet pad pump from zones B and C to relay 6 (129,152)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(channel_pump, GPIO.OUT)


# Define functions for each device
#wet pad pump
def pump_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def pump_on(pin):
    GPIO.output(pin, GPIO.LOW)


# Define functions to control devices in threads

def pump_thread():
    while True:
        current_time = datetime.now().time()

        if time(6, 0) <= current_time <= time(18, 0):
            pump_on(channel_pump)
        else:
            pump_off(channel_pump)
            
            

try:
    # Start threads for each device
    threading.Thread(target=pump_thread).start()


    # Keep the main thread running
    while True:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
