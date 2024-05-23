import RPi.GPIO as GPIO
from datetime import datetime, time
import threading
import time as t

# Define GPIO channels
channel_fan1 = 25  # connect the set 1 of fans from zone B and C to relay1 (147,179)
channel_fan2 = 24  # connect the set 2 of fans from zone B and C to relay2 (148,180)
channel_pump = 14 #connect the wet pad pump from zones B and C to relay 6 (129,152)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(channel_fan1, GPIO.OUT)
GPIO.setup(channel_fan2, GPIO.OUT)
GPIO.setup(channel_pump, GPIO.OUT)
# Define functions for each device


# fan1
def fan1_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def fan1_on(pin):
    GPIO.output(pin, GPIO.LOW)

# fan2
def fan2_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def fan2_on(pin):
    GPIO.output(pin, GPIO.LOW)

#pump
def pump_off(pin):
    GPIO.output(pin, GPIO.HIGH)
def pump_on(pin):
    GPIO.output(pin, GPIO.LOW)


# fans are delayed by 2 seconds to prevent electrical surge
def fan1_thread():
    while True:
        current_time = datetime.now().time()
        current_date = datetime.now().date()

        if current_time >= time(16, 30) and current_time < time(18, 0) and current_date == datetime(2024, 2, 28).date():
            fan1_off(channel_fan1)
            fan2_off(channel_fan2)
        elif current_time >= time(18, 0) and current_time < time(23, 59) and current_date == datetime(2024, 2, 28).date():
            fan1_on(channel_fan1)
            fan2_on(channel_fan2)
        elif current_time >= time(0, 0) and current_time < time(3, 0) and current_date == datetime(2024, 2, 29).date():
            fan1_off(channel_fan1)
            fan2_off(channel_fan2)
        elif current_time >= time(3, 0) and current_time < time(7, 0) and current_date == datetime(2024, 2, 29).date():
            fan1_on(channel_fan1)
            fan2_off(channel_fan2)
        elif current_time >= time(7, 0) and current_time < time(8, 30) and current_date == datetime(2024, 2, 29).date():
            fan1_off(channel_fan1)
            fan2_off(channel_fan2)
        elif current_time >= time(8, 30) and current_time < time(10, 0) and current_date == datetime(2024, 2, 29).date():
            fan1_on(channel_fan1)
            fan2_off(channel_fan2)
        elif current_time >= time(10, 0) and current_date == datetime(2024, 2, 29).date():
            fan1_on(channel_fan1)
            fan2_on(channel_fan2)
        else:
            fan1_on(channel_fan1)
            fan2_on(channel_fan2)

        t.sleep(0.5)

def pump_thread():
    while True:
        current_time = datetime.now().time()

        if time(9, 0, 0) <= current_time <= time(20, 0, 0):
            pump_on(channel_pump)
            t.sleep(5)
        else:
            pump_off(channel_pump)
            t.sleep(5)
            
            
try:
    # Start threads for each device

    threading.Thread(target=fan1_thread).start()
    threading.Thread(target=pump_thread).start()


    # Keep the main thread running
    while True:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()
