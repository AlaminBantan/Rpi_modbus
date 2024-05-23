import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Specify the new full path to your CSV file
csv_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\Phenotyipic data zone c.csv"

# Read the CSV file
df = pd.read_csv(csv_path)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Define custom colors for each Treatment
custom_palette = {'CC3': 'blue', 'CC4': 'lightblue', 'CM3': '#FFD700', 'CM4': 'orange'}

# Create a box plot using seaborn with custom colors
plt.figure(figsize=(12, 8))
ax = sns.boxplot(x=df['Date'].dt.date, y='Plant height (cm)', hue='Treatment', data=df, palette=custom_palette)
plt.title('Stem elongation in Zone C')
plt.xlabel('Date')
plt.ylabel('Plant Height (cm)')
plt.xticks(rotation=45)

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Save the figure as an SVG file
output_folder = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\Zone C"
output_filename = "stem_elongation_zone_C.svg"
output_filepath = os.path.join(output_folder, output_filename)

plt.savefig(output_filepath, format='svg', bbox_inches='tight')
plt.show()
