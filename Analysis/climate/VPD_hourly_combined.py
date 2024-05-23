# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:15:22 2024

@author: bantanam
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file
csv_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_VPD_data.csv"
df = pd.read_csv(csv_path)

# Convert 'date' and 'time' columns to datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Group by hour and calculate the mean for Mean zone B and Mean zone C
hourly_mean = df.groupby(df['datetime'].dt.hour)[['Mean zone B', 'Mean zone C']].mean()

# Output folder for saving SVG plots
output_folder = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\VPD"

# Ensure the output folder exists, create it if not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Plotting both Mean zone B and Mean zone C in one figure
plt.figure(figsize=(10, 6))
plt.plot(hourly_mean['Mean zone B'], label='Mean zone B', color='blue')
plt.plot(hourly_mean['Mean zone C'], label='Mean zone C', color='green')

plt.title('Average VPD for Zones B and C by Hour')
plt.xlabel('Hour')
plt.ylabel('VPD (kPa)')
plt.legend()
plt.grid(True)  # Optional: Adds grid lines for better readability

# Save the combined plot as SVG
plt.savefig(os.path.join(output_folder, 'average_vpd_zones_b_and_c.svg'))
plt.close()
