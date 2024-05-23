

import pandas as pd
import matplotlib.pyplot as plt

# Read CSV files
df_north = pd.read_csv(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\north_modified.csv")
df_south = pd.read_csv(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\south_modified.csv")

# Convert 'datetime' column to datetime type
df_north['datetime'] = pd.to_datetime(df_north['datetime'])
df_south['datetime'] = pd.to_datetime(df_south['datetime'])

# Calculate daily minimum, maximum, and mean values for temperature and humidity
df_north_daily = df_north.groupby(df_north['datetime'].dt.date).agg({
    'Temperature_north (c)': ['min', 'max', 'mean'],
    'Humidity_north (%)': ['min', 'max', 'mean']
}).reset_index()

df_south_daily = df_south.groupby(df_south['datetime'].dt.date).agg({
    'Temperature_south (c)': ['min', 'max', 'mean'],
    'Humidity_south (%)': ['min', 'max', 'mean']
}).reset_index()

# Plot temperature
plt.figure(figsize=(10, 6))

plt.plot(df_north_daily['datetime'], df_north_daily['Temperature_north (c)']['min'], color='red', linestyle=':', label='North Min')
plt.plot(df_north_daily['datetime'], df_north_daily['Temperature_north (c)']['max'], color='red', linestyle='--', label='North Max')
plt.plot(df_north_daily['datetime'], df_north_daily['Temperature_north (c)']['mean'], color='red', linestyle='-', label='North Mean')

plt.plot(df_south_daily['datetime'], df_south_daily['Temperature_south (c)']['min'], color='blue', linestyle=':', label='South Min')
plt.plot(df_south_daily['datetime'], df_south_daily['Temperature_south (c)']['max'], color='blue', linestyle='--', label='South Max')
plt.plot(df_south_daily['datetime'], df_south_daily['Temperature_south (c)']['mean'], color='blue', linestyle='-', label='South Mean')

plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.ylim((10,50))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\Temperature_mean.png")
plt.show()

# Plot humidity
plt.figure(figsize=(10, 6))

plt.plot(df_north_daily['datetime'], df_north_daily['Humidity_north (%)']['min'], color='red', linestyle=':', label='North Min')
plt.plot(df_north_daily['datetime'], df_north_daily['Humidity_north (%)']['max'], color='red', linestyle='--', label='North Max')
plt.plot(df_north_daily['datetime'], df_north_daily['Humidity_north (%)']['mean'], color='red', linestyle='-', label='North Mean')

plt.plot(df_south_daily['datetime'], df_south_daily['Humidity_south (%)']['min'], color='blue', linestyle=':', label='South Min')
plt.plot(df_south_daily['datetime'], df_south_daily['Humidity_south (%)']['max'], color='blue', linestyle='--', label='South Max')
plt.plot(df_south_daily['datetime'], df_south_daily['Humidity_south (%)']['mean'], color='blue', linestyle='-', label='South Mean')

plt.xlabel('Date')
plt.ylabel('Humidity (%)')
plt.title('Humidity Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.ylim((0,100))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\Humidity_mean.png")
plt.show()
