import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from the CSV file
csv_path = r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Humidity_data.csv'
df = pd.read_csv(csv_path, parse_dates=['date'], infer_datetime_format=True)

# Extract date from datetime
df['date'] = df['date'].dt.date

# Group data by Date for Zone B and Zone C
zone_b_grouped = df.groupby(['date', 'time'])[['Zone B subzone 1', 'Zone B subzone 2', 'Mean zone B']].mean()
zone_c_grouped = df.groupby(['date', 'time'])[['Zone C subzone 1', 'Zone C subzone 2', 'Mean zone C']].mean()

# Create plots for each day in Zone B
for date, group_data in zone_b_grouped.groupby('date'):
    plt.figure(figsize=(15, 10))  # Adjusted width
    
    for subzone in ['Zone B subzone 1', 'Zone B subzone 2']:
        plt.plot(group_data.index.get_level_values('time'), group_data[subzone], label=f'Zone B {subzone}')

    plt.plot(group_data.index.get_level_values('time'), group_data['Mean zone B'], label='Zone B Mean', linestyle='--', color='black')

    plt.title(f'Daily humidity Zone B - {date}')
    plt.xlabel('Time')
    plt.ylabel('RH (%)')
    
    # Set vertical time ticks
    plt.xticks(rotation='vertical', fontsize=8)
    # Set y-axis limits
    plt.ylim(30, 100)

    plt.legend()
    
    file_name = f'Daily_humidity_Zone_B_{date}.png'
    file_path = r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Humidity\\' + file_name
    plt.savefig(file_path)
    plt.close()

# Create plots for each day in Zone C
for date, group_data in zone_c_grouped.groupby('date'):
    plt.figure(figsize=(15, 10))  # Adjusted width
    
    for subzone in ['Zone C subzone 1', 'Zone C subzone 2']:
        plt.plot(group_data.index.get_level_values('time'), group_data[subzone], label=f'Zone C {subzone}')

    plt.plot(group_data.index.get_level_values('time'), group_data['Mean zone C'], label='Zone C Mean', linestyle='--', color='black')

    plt.title(f'Daily humidity Zone C - {date}')
    plt.xlabel('Time')
    plt.ylabel('RH (%)')
    
    # Set vertical time ticks
    plt.xticks(rotation='vertical', fontsize=8)
    # Set y-axis limits
    plt.ylim(30, 100)

    plt.legend()
    
    file_name = f'Daily_humidity_Zone_C_{date}.png'
    file_path = r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Humidity\\' + file_name
    plt.savefig(file_path)
    plt.close()
