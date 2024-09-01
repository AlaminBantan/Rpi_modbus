import pandas as pd
import time
import RPi.GPIO as GPIO
from datetime import datetime
import logging

# Setup GPIO
RELAY_PIN = 17  # Use the GPIO pin you have connected the relay to
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(RELAY_PIN, GPIO.OUT)

# File path
CSV_FILE_PATH = '/home/cdacea/south_GH/south_climate.csv'

# Setup logging
LOG_FILE_PATH = '/home/cdacea/south_GH/relay_control.log'
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(message)s')

def read_csv_and_control_relay():
    # Read the CSV file, suppress dtype warnings
    df = pd.read_csv(CSV_FILE_PATH, low_memory=False)
    
    # Get the latest row
    latest_row = df.iloc[-1]
    
    # Get the CO2 concentration, convert to a number
    try:
        co2_concentration = float(latest_row['CO2 conc_south (ppm)'])
        logging.info(f"CO2 concentration read: {co2_concentration} ppm")
    except ValueError:
        logging.warning("CO2 concentration is not a number. Skipping this row.")
        return
    
    # Control the relay
    if co2_concentration < 800:
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn on the relay
        logging.info(f"CO2 concentration {co2_concentration} ppm - Relay turned ON for 5 seconds.")
        time.sleep(5)  # Keep the relay on for 5 seconds
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the relay
    elif co2_concentration > 1100:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the relay
        logging.info(f"CO2 concentration {co2_concentration} ppm - Relay turned OFF.")

try:
    while True:
        current_time = datetime.now().time()
        if current_time >= datetime.strptime("08:00:00", "%H:%M:%S").time() and current_time <= datetime.strptime("17:00:00", "%H:%M:%S").time():
            read_csv_and_control_relay()
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Ensure the relay is turned off outside the specified hours
            logging.info("Outside working hours - Relay turned OFF.")
        time.sleep(60)  # Wait for 1 minute
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
    logging.info("Program terminated and GPIO cleaned up.")
