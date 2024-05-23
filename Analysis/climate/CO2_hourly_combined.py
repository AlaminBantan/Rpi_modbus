# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:18:29 2024

@author: bantanam
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file
csv_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_CO2Conc_data.csv"
df = pd.read_csv(csv_path)

# Convert 'date' and 'time' columns to datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Group by hour and calculate the mean for Zone B subzone 1 and Zone C subzone 1
hourly_mean = df.groupby(df['datetime'].dt.hour)[['Zone B subzone 1', 'Zone C subzone 1']].mean()

# Output folder for saving SVG plots
output_folder = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\CO2 conc"

# Ensure the output folder exists, create it if not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Plotting both Zone B subzone 1 and Zone C subzone 1 in one figure
plt.figure(figsize=(10, 6))
plt.plot(hourly_mean['Zone B subzone 1'], label='Zone B subzone 1', color='blue')
plt.plot(hourly_mean['Zone C subzone 1'], label='Zone C subzone 1', color='green')

plt.title('Average CO2 Concentration for Zones B and C Subzones')
plt.xlabel('Hour')
plt.ylabel('CO2 Concentration (ppm)')
plt.ylim(350, 450)  # Adjust the y-axis limits if necessary
plt.legend()
plt.grid(True)  # Optional, but improves readability

# Save the combined plot as SVG
plt.savefig(os.path.join(output_folder, 'average_co2_zones_b_and_c_subzones.svg'))
plt.close()
