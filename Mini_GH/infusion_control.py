import time
import RPi.GPIO as GPIO
from datetime import datetime, time as dt_time
import logging

# Setup GPIO
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # Ensure relay is off at start

# Setup logging
LOG_FILE_PATH = '/home/cdacea/south_GH/relay_control.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(message)s')

# Define schedule: from 07:50 to 17:00
START_HOUR = 7
START_MINUTE = 50
END_HOUR = 17
ON_DURATION_MINUTES = 10
INTERVAL_MINUTES = 60

def is_within_on_period(now):
    """
    Returns True if current time is within the 10-minute ON period of any hour interval
    starting from 7:50 AM to 5:00 PM.
    """
    start_time = dt_time(START_HOUR, START_MINUTE)
    end_time = dt_time(END_HOUR, 0)

    if now.time() < start_time or now.time() > end_time:
        return False

    minutes_since_start = (now.hour * 60 + now.minute) - (START_HOUR * 60 + START_MINUTE)
    return (minutes_since_start % INTERVAL_MINUTES) < ON_DURATION_MINUTES

try:
    while True:
        now = datetime.now()
        if is_within_on_period(now):
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn ON
            logging.info("Scheduled ON period - Relay turned ON.")
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn OFF
            logging.info("Outside ON period - Relay turned OFF.")
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    pass
finally:
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    GPIO.cleanup()
    logging.info("Program terminated and GPIO cleaned up.")
