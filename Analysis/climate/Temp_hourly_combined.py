# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:21:27 2024

@author: bantanam
"""

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Temperature_data.csv"
df = pd.read_csv(file_path)

# Combine date and time columns into a single datetime column
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Set the datetime column as the index
df.set_index('datetime', inplace=True)

# Calculate the hourly average of Mean Zone B and Mean Zone C
hourly_average = df.groupby(df.index.hour).agg({'Mean zone B': 'mean', 'Mean zone C': 'mean'})

# Plot the hourly averages for Mean Zone B and Mean Zone C on the same figure
plt.figure(figsize=(15, 10))
plt.plot(hourly_average['Mean zone B'], label='Mean Zone B', linestyle='-', color='blue')
plt.plot(hourly_average['Mean zone C'], label='Mean Zone C', linestyle='-', color='green')

plt.title('Hourly Average Temperature for Zones B and C')
plt.xlabel('Time (hours)')
plt.ylabel('Average Temperature (°C)')
plt.ylim(10, 40)  # Adjust the y-axis limits if necessary
plt.legend()
plt.grid(True)  # Optional: Adds grid lines for better readability

# Save the combined plot in the specified directory
output_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Temp"
if not os.path.exists(output_path):
    os.makedirs(output_path)
plt.savefig(os.path.join(output_path, 'Hourly_Average_Temperature_Zones_B_and_C.svg'))

# Show the plot
plt.show()
