import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\data yeild.csv"
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sort the DataFrame by date
df = df.sort_values(by='Date')

# Plot the average weight of fruits for each treatment with specified colors
plt.figure(figsize=(10, 6))
for treatment, data in df.groupby('Treatment'):
    if treatment == 'Control':
        plt.plot(data['Date'], data['Average fruit (g/fruit)'], label=f'{treatment} - Avg Weight', color='blue')
    elif treatment == 'Misting':
        plt.plot(data['Date'], data['Average fruit (g/fruit)'], label=f'{treatment} - Avg Weight', color='#FFD700')

plt.xlabel('Date')
plt.ylabel('Average Weight of Fruits (g/fruit)')
plt.title('Average Weight of Fruits for Each Treatment Over Time')
plt.xticks(rotation=45)
plt.legend()

# Save the plot as an SVG file
save_path_avg_weight = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\average_weight_plot.svg"
plt.savefig(save_path_avg_weight)

# Show the plot
plt.show()
