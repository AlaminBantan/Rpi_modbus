import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate
import time

# Define the path to your CSV file
csv_file_path = '/home/cdacea/north_GH/north_climate.csv'

def display_recent_data():
    # Read the CSV file
    data = pd.read_csv(csv_file_path)

    # Convert the 'datetime' column to datetime objects
    data['datetime'] = pd.to_datetime(data['datetime'])

    # Get the current time
    now = datetime.now()

    # Define the time range for the last 5 minutes
    time_threshold = now - timedelta(minutes=5)

    # Filter the data to get only the records from the last 5 minutes
    recent_data = data[data['datetime'] >= time_threshold]

    # Clear the screen
    print("\033c", end="")

    # Display the recent data in a tabular format
    print(tabulate(recent_data, headers='keys', tablefmt='grid'))

if __name__ == "__main__":
    while True:
        display_recent_data()
        time.sleep(60)  # Wait for 1 minute before updating again
