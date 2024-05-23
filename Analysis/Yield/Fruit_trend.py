# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 14:46:30 2024

@author: bantanam
"""

import pandas as pd
import matplotlib.pyplot as plt

# File paths
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\data yeild.csv"
save_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\yield_trend.svg"

# Custom color palette
custom_palette = {'Control': 'blue', 'Misting': '#FFD700'}

# Read the CSV file
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Group the data by treatment type
grouped = df.groupby('Treatment')

# Plot the data for each treatment using custom colors
plt.figure(figsize=(10, 6))
for treatment, group in grouped:
    plt.plot(group['Date'], group['# fruits'], label=treatment, color=custom_palette.get(treatment))

# Add labels and title
plt.xlabel('Date')
plt.ylabel('# Fruits')
plt.title('Yield Comparison by Treatment')
plt.legend()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show plot
plt.grid(True)
plt.tight_layout()

# Save plot as SVG
plt.savefig(save_path, format='svg')

# Show plot
plt.show()
