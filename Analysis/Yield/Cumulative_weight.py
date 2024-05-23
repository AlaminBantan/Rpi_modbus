import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\data yeild.csv"
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sort the DataFrame by date
df = df.sort_values(by='Date')

# Calculate cumulative weight for each treatment
df['Cumulative Weight'] = df.groupby('Treatment')['Weight (g)'].cumsum()

# Plot the cumulative weight for each treatment with specified colors
plt.figure(figsize=(10, 6))
for treatment, data in df.groupby('Treatment'):
    if treatment == 'Control':
        plt.plot(data['Date'], data['Cumulative Weight'], label=treatment, color='blue')
    elif treatment == 'Misting':
        plt.plot(data['Date'], data['Cumulative Weight'], label=treatment, color='#FFD700')

plt.xlabel('Date')
plt.ylabel('Cumulative Weight (g)')
plt.title('Cumulative Weight of Each Treatment Over Time')
plt.xticks(rotation=45)
plt.legend()

# Save the plot as an SVG file
save_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\cumulative_weight_plot.svg"
plt.savefig(save_path)

# Show the plot
plt.show()
