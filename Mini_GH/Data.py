import pandas as pd
from datetime import datetime, timedelta
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

    # Define the time range for the last 1 minute
    time_threshold = now - timedelta(minutes=1)

    # Filter the data to get only the records from the last 1 minute
    recent_data = data[data['datetime'] >= time_threshold]

    # Clear the screen
    print("\033c", end="")

    # Print the recent data in the specified format
    for index, row in recent_data.iterrows():
        time_str = row['datetime'].strftime('%H:%M')
        print(f" Time: {time_str}")
        print(f" PAR: {row['PAR_north (umol.m-1.s-1)']} umol.m-1.s-1")
        print(f" Solar radiation: {row['Solar radiation_north (w.m-2)']} w.m-2")
        print(f" Temperature: {row['Temperature_north (c)']} C")
        print(f" Humidity: {row['Humidity_north (%)']} %")
        print(f" CO2 concentration: {row['CO2 conc_north (ppm)']} ppm")
        
        print("-" * 30)  # Separator between records

if __name__ == "__main__":
    while True:
        display_recent_data()
        time.sleep(60)  # Wait for 1 minute before updating again

