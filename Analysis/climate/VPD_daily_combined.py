# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:28:20 2024

@author: bantanam
"""

import pandas as pd
import matplotlib.pyplot as plt

# Specify the path to your CSV file
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_VPD_data.csv"

# Load the CSV data into a DataFrame
df = pd.read_csv(file_path)

# Ensure the 'date' column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Calculate the daily average, minimum, and maximum for Mean Zone B and Mean Zone C
daily_stats = df.groupby(df['date'].dt.date).agg({
    'Mean zone B': ['mean', 'min', 'max'],
    'Mean zone C': ['mean', 'min', 'max']
}).reset_index()

# Flatten the MultiIndex for easier plotting
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
ax.set_ylabel('VPD')
ax.set_title('Daily VPD Stats for Zones B and C')
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\VPD\Daily_Average_Mean_Zone_B_and_C.svg")
# Show the plot
plt.show()
