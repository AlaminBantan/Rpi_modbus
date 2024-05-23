import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\data yeild.csv"
df = pd.read_csv(file_path)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Sort the DataFrame by date
df = df.sort_values(by='Date')

# Calculate cumulative number of fruits for each treatment
df['Cumulative Fruits'] = df.groupby('Treatment')['# fruits'].cumsum()

# Plot the cumulative number of fruits for each treatment with specified colors
plt.figure(figsize=(10, 6))
for treatment, data in df.groupby('Treatment'):
    if treatment == 'Control':
        plt.plot(data['Date'], data['Cumulative Fruits'], label=f'{treatment} - Fruits', color='blue')
    elif treatment == 'Misting':
        plt.plot(data['Date'], data['Cumulative Fruits'], label=f'{treatment} - Fruits', color='#FFD700')

plt.xlabel('Date')
plt.ylabel('Cumulative Number of Fruits')
plt.title('Cumulative Number of Fruits for Each Treatment Over Time')
plt.xticks(rotation=45)
plt.legend()

# Save the plot as an SVG file
save_path_fruits = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Results\cumulative_fruits_plot.svg"
plt.savefig(save_path_fruits)

# Show the plot
plt.show()
