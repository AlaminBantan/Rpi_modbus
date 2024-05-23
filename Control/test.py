import RPi.GPIO as GPIO
from datetime import datetime, time
import time as t
import threading


channel_24 = 24
channel_25 = 25

# GPIO setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(channel_24, GPIO.OUT)
GPIO.setup(channel_25, GPIO.OUT)

def motor_off(pin):
    GPIO.output(pin, GPIO.HIGH)

def motor_on(pin):
    GPIO.output(pin, GPIO.LOW)

def motor_thread(pin, name):
    try:
        while True:
            print(f"Motor {name} is low")
            motor_on(pin)
            t.sleep(10)
            print(f"Motor {name} is high")
            motor_off(pin)
            t.sleep(10)
    except KeyboardInterrupt:
        GPIO.cleanup()

# Create threads for each motor

motor_24_thread = threading.Thread(target=motor_thread, args=(channel_24, "24"))
motor_25_thread = threading.Thread(target=motor_thread, args=(channel_25, "25"))

try:
    # Start the threads

    motor_24_thread.start()
    motor_25_thread.start()

    # Wait for all threads to finish

    motor_24_thread.join()
    motor_25_thread.join()

except KeyboardInterrupt:
    GPIO.cleanup()

