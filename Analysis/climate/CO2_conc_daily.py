import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from the CSV file
csv_path = r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_CO2Conc_data.csv'
df = pd.read_csv(csv_path, parse_dates=['date'], infer_datetime_format=True)

# Extract date from datetime
df['date'] = df['date'].dt.date

# Group data by Date for Zone B and Zone C
zone_b_grouped = df.groupby(['date', 'time'])[['Zone B subzone 1']].mean()
zone_c_grouped = df.groupby(['date', 'time'])[['Zone C subzone 1']].mean()

# Create plots for each day in Zone B
for date, group_data in zone_b_grouped.groupby('date'):
    plt.figure(figsize=(15, 10))  # Adjusted width
    
    for subzone in ['Zone B subzone 1']:
        plt.plot(group_data.index.get_level_values('time'), group_data[subzone], label=f'Zone B {subzone}')



    plt.title(f'Daily CO2 concentration Zone B - {date}')
    plt.xlabel('Time')
    plt.ylabel('CO2 (ppm)')
    
    # Set vertical time ticks
    plt.xticks(rotation='vertical', fontsize=8)


    plt.legend()
    
    file_name = f'Daily_CO2_Zone_B_{date}.png'
    file_path = r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\CO2 conc\\' + file_name
    plt.savefig(file_path)
    plt.close()

# Create plots for each day in Zone C
for date, group_data in zone_c_grouped.groupby('date'):
    plt.figure(figsize=(15, 10))  # Adjusted width
    
    for subzone in ['Zone C subzone 1']:
        plt.plot(group_data.index.get_level_values('time'), group_data[subzone], label=f'Zone C {subzone}')


    plt.title(f'Daily CO2 concentration Zone C - {date}')
    plt.xlabel('Time')
    plt.ylabel('CO2 (ppm)')
    
    # Set vertical time ticks
    plt.xticks(rotation='vertical', fontsize=8)
 
    plt.legend()
    
    file_name = f'Daily_CO2_Zone_C_{date}.png'
    file_path = r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\CO2 conc\\' + file_name
    plt.savefig(file_path)
    plt.close()
