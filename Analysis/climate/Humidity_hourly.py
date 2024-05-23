import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Humidity_data.csv"
df = pd.read_csv(file_path)

# Combine date and time columns into a single datetime column
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Set the datetime column as the index
df.set_index('datetime', inplace=True)

# Calculate the hourly average of Mean Zone B and Mean Zone C
hourly_average_B = df.groupby(df.index.hour).agg({'Mean zone B': 'mean'})
hourly_average_C = df.groupby(df.index.hour).agg({'Mean zone C': 'mean'})

# Plot the hourly averages for Mean Zone B
plt.figure(figsize=(15, 10))
hourly_average_B.plot(linestyle='-', color='blue')
plt.title('Hourly Average Humidity of Zone B')
plt.xlabel('Time (hours)')
plt.ylabel('RH (%)')
plt.ylim(30, 100)


# Save the plot in the specified directory
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Humidity\Hourly_Average_Mean_Zone_B.svg")

# Show the plot
plt.show()

# Plot the hourly averages for Mean Zone C
plt.figure(figsize=(15, 10))
hourly_average_C.plot(linestyle='-', color='green')
plt.title('Hourly Average Humidity of Zone C')
plt.xlabel('Time (hours)')
plt.ylabel('RH (%)')
plt.ylim(30, 100)

# Save the plot in the specified directory
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Humidity\Hourly_Average_Mean_Zone_C.svg")

# Show the plot
plt.show()
