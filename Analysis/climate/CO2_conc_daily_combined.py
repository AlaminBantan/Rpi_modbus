# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:40:23 2024

@author: bantanam
"""

import pandas as pd
import matplotlib.pyplot as plt

# Specify the path to your CSV file
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_CO2Conc_data.csv"

# Load the CSV data into a DataFrame
df = pd.read_csv(file_path)

# Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Calculate the daily average, minimum, and maximum for Zone B subzone 1 and Zone C subzone 1
daily_stats = df.groupby(df['date'].dt.date).agg({
    'Zone B subzone 1': ['mean', 'min', 'max'],
    'Zone C subzone 1': ['mean', 'min', 'max']
}).reset_index()

# Flatten the MultiIndex for easier plotting
daily_stats.columns = [' '.join(col).strip() for col in daily_stats.columns.values]

# Setting up the figure and axes for plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plotting Zone B subzone 1
ax.plot(daily_stats['date'], daily_stats['Zone B subzone 1 mean'], label='Average Zone B subzone 1', marker='o', color='blue')
ax.fill_between(daily_stats['date'], daily_stats['Zone B subzone 1 min'], daily_stats['Zone B subzone 1 max'], color='blue', alpha=0.1)

# Plotting Zone C subzone 1
ax.plot(daily_stats['date'], daily_stats['Zone C subzone 1 mean'], label='Average Zone C subzone 1', marker='o', color='green',)
ax.fill_between(daily_stats['date'], daily_stats['Zone C subzone 1 min'], daily_stats['Zone C subzone 1 max'], color='green', alpha=0.1)

# Formatting the plot
ax.set_xlabel('Date')
ax.set_ylabel('CO2 Concentration')
ax.set_title('Daily CO2 Concentration Stats for Zone B and Zone C subzone 1')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
# Save the plot in the specified directory
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\CO2 conc\Daily_Average_Mean_Zone_B_and_C.svg")
# Show the plot
plt.show()
