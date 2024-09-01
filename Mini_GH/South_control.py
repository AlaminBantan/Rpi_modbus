import pandas as pd
import time
import RPi.GPIO as GPIO
from datetime import datetime

# Setup GPIO
RELAY_PIN = 17  # Use the GPIO pin you have connected the relay to
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# File path
CSV_FILE_PATH = '/home/cdacea/south_GH/south_climate.csv'

def read_csv_and_control_relay():
    # Read the CSV file
    df = pd.read_csv(CSV_FILE_PATH)
    
    # Get the latest row
    latest_row = df.iloc[-1]
    
    # Get the CO2 concentration
    co2_concentration = latest_row['CO2 conc_south (ppm)']
    
    # Control the relay
    if co2_concentration < 800:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn on the relay
        time.sleep(5)  # Keep the relay on for 5 seconds
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn off the relay
    elif co2_concentration > 1100:
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn off the relay

try:
    while True:
        current_time = datetime.now().time()
        if current_time >= datetime.strptime("08:00:00", "%H:%M:%S").time() and current_time <= datetime.strptime("17:00:00", "%H:%M:%S").time():
            read_csv_and_control_relay()
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Ensure the relay is turned off outside the specified hours
        time.sleep(60)  # Wait for 1 minute
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
