import pandas as pd
import matplotlib.pyplot as plt

# Load CSV into DataFrame
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Temperature_data.csv"
df = pd.read_csv(file_path)

# Combine 'date' and 'time' columns and convert to datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Set 'datetime' as the index
df.set_index('datetime', inplace=True)

# Create a new column for the hour of the day
df['hour'] = df.index.hour

# Filter data for the time range between 6 am and 6 pm
filtered_df_day = df[(df['hour'] >= 6) & (df['hour'] <= 18)]

# Calculate the mean temperature for Zone B and Zone C for each day
daily_mean_zone_b_c = filtered_df_day.groupby(filtered_df_day.index.date)[['Mean zone B', 'Mean zone C']].mean()

# Plotting and Saving Zone B for Day
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_mean_zone_b_c.index, daily_mean_zone_b_c['Mean zone B'], label='Daytime Zone B', color='blue')

# Filter data for the time range between 6 pm and 6 am
filtered_df_night = df[(df['hour'] < 6) | (df['hour'] >= 18)]

# Calculate the mean temperature for Zone B for each night
nightly_mean_zone_b = filtered_df_night.groupby(filtered_df_night.index.date)['Mean zone B'].mean()

# Plotting and Saving Zone B for Night
ax.plot(nightly_mean_zone_b.index, nightly_mean_zone_b, label='Nighttime Zone B', color='red')

ax.set_title('Mean Temperature - Zone B')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')
ax.legend()
plt.tight_layout()
save_path_zone_b_combined = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Temp\combined_mean_temperature_zone_b.png"
plt.savefig(save_path_zone_b_combined)
plt.close()

# Calculate the mean temperature for Zone C for each day
daily_mean_zone_c_c = filtered_df_day.groupby(filtered_df_day.index.date)[['Mean zone C']].mean()

# Plotting and Saving Zone C for Day
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_mean_zone_c_c.index, daily_mean_zone_c_c['Mean zone C'], label='Daytime Zone C', color='green')

# Calculate the mean temperature for Zone C for each night
nightly_mean_zone_c = filtered_df_night.groupby(filtered_df_night.index.date)['Mean zone C'].mean()

# Plotting and Saving Zone C for Night
ax.plot(nightly_mean_zone_c.index, nightly_mean_zone_c, label='Nighttime Zone C', color='red')

ax.set_title('Mean Temperature - Zone C')
ax.set_xlabel('Date')
ax.set_ylabel('Temperature (°C)')
ax.legend()
plt.tight_layout()
save_path_zone_c_combined = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Temp\combined_mean_temperature_zone_c.png"
plt.savefig(save_path_zone_c_combined)
plt.close()
