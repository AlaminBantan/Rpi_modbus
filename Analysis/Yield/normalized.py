import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
csv_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\normalized.csv"
df = pd.read_csv(csv_path)

# Convert 'week' values to integers
df['week'] = df['week'].astype(int)

# Calculate average yield and standard deviation for each treatment and week
grouped_data = df.groupby(['week', 'treatment'])['yield (kg/m2)']
average_yield_per_treatment = grouped_data.mean().unstack()
std_dev_per_treatment = grouped_data.std().unstack()

# Define custom color palette
custom_palette = {'Control': 'blue', 'Misting': '#FFD700'}

# Plotting the line graph for each treatment with error bars (standard deviation)
plt.figure(figsize=(10, 6))

for treatment in average_yield_per_treatment.columns:
    plt.errorbar(average_yield_per_treatment.index, average_yield_per_treatment[treatment],
                 yerr=std_dev_per_treatment[treatment], marker='o', label=treatment, color=custom_palette.get(treatment))

plt.title('Average Yield Comparison Across Treatments')
plt.xlabel('Week')
plt.ylabel('Average Yield (kg/m2)')
plt.xticks(average_yield_per_treatment.index)  # Ensure x-axis ticks include only integers
plt.legend()
plt.grid(True)

# Save the plot as an SVG file
svg_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\average_yield_comparison.svg"
plt.savefig(svg_path, format='svg')

plt.show()
