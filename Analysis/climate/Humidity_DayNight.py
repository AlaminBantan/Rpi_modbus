import pandas as pd
import matplotlib.pyplot as plt

# Load CSV into DataFrame
file_path_humidity = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Humidity_data.csv"
df_humidity = pd.read_csv(file_path_humidity)

# Combine 'date' and 'time' columns and convert to datetime
df_humidity['datetime'] = pd.to_datetime(df_humidity['date'] + ' ' + df_humidity['time'])

# Set 'datetime' as the index
df_humidity.set_index('datetime', inplace=True)

# Create a new column for the hour of the day
df_humidity['hour'] = df_humidity.index.hour

# Filter data for the time range between 6 am and 6 pm
filtered_df_humidity_day = df_humidity[(df_humidity['hour'] >= 6) & (df_humidity['hour'] <= 18)]

# Calculate the mean humidity for Zone B and Zone C for each day
daily_mean_humidity_zone_b_c = filtered_df_humidity_day.groupby(filtered_df_humidity_day.index.date)[['Mean zone B', 'Mean zone C']].mean()

# Filter data for the time range between 6 pm and 6 am
filtered_df_humidity_night = df_humidity[(df_humidity['hour'] < 6) | (df_humidity['hour'] >= 18)]

# Calculate the mean humidity for Zone B for each night
nightly_mean_humidity_zone_b = filtered_df_humidity_night.groupby(filtered_df_humidity_night.index.date)['Mean zone B'].mean()

# Calculate the mean humidity for Zone C for each night
nightly_mean_humidity_zone_c = filtered_df_humidity_night.groupby(filtered_df_humidity_night.index.date)['Mean zone C'].mean()

# Plotting and Saving Zone B
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_mean_humidity_zone_b_c.index, daily_mean_humidity_zone_b_c['Mean zone B'], label='Daytime Zone B', color='blue')
ax.plot(nightly_mean_humidity_zone_b.index, nightly_mean_humidity_zone_b, label='Nighttime Zone B', color='navy', linestyle='dashed')
ax.set_title('Mean Humidity - Zone B')
ax.set_xlabel('Date')
ax.set_ylabel('Humidity (%)')
plt.ylim(30, 100)
ax.legend()
plt.tight_layout()
save_path_humidity_zone_b = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Humidity\mean_humidity_zone_b.png"
plt.savefig(save_path_humidity_zone_b)
plt.close()

# Plotting and Saving Zone C
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_mean_humidity_zone_b_c.index, daily_mean_humidity_zone_b_c['Mean zone C'], label='Daytime Zone C', color='green')
ax.plot(nightly_mean_humidity_zone_c.index, nightly_mean_humidity_zone_c, label='Nighttime Zone C', color='darkgreen', linestyle='dashed')
ax.set_title('Mean Humidity - Zone C')
ax.set_xlabel('Date')
ax.set_ylabel('Humidity (%)')
plt.ylim(30, 100)
ax.legend()
plt.tight_layout()
save_path_humidity_zone_c = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Humidity\mean_humidity_zone_c.png"
plt.savefig(save_path_humidity_zone_c)
plt.close()
