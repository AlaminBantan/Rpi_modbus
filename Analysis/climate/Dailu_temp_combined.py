# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:06:10 2024

@author: bantanam
"""

import pandas as pd
import matplotlib.pyplot as plt

# Specify the path to your CSV file
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Temperature_data.csv"

# Load the CSV data into a DataFrame
df = pd.read_csv(file_path)

# Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Group by date and calculate the average, min, and max for each zone
daily_stats = df.groupby(df['date'].dt.date).agg({
    'Mean zone B': ['mean', 'min', 'max'],
    'Mean zone C': ['mean', 'min', 'max']
}).reset_index()

# The 'daily_stats' DataFrame has a MultiIndex for the columns after aggregation.
# You might need to adjust column names for plotting.
# This step flattens the MultiIndex for ease of use.
daily_stats.columns = [' '.join(col).strip() for col in daily_stats.columns.values]

# Setting up the figure and axes for plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting Mean Zone B
ax.plot(daily_stats['date'], daily_stats['Mean zone B mean'], label='Average Zone B', marker='o', color='blue')
ax.fill_between(daily_stats['date'], daily_stats['Mean zone B min'], daily_stats['Mean zone B max'], color='blue', alpha=0.1)

# Plotting Mean Zone C
ax.plot(daily_stats['date'], daily_stats['Mean zone C mean'], label='Average Zone C', marker='o', color='green')
ax.fill_between(daily_stats['date'], daily_stats['Mean zone C min'], daily_stats['Mean zone C max'], color='green', alpha=0.1)

# Formatting the plot
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Daily Temperature Stats for Zones B and C')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Temp\Daily_Average_Mean_Zone_B_and_C.svg")

# Show the plot
plt.show()
