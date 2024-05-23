import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load data from CSV file
csv_file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Temperature_data.csv"
df = pd.read_csv(csv_file_path)

# Convert 'date' and 'time' columns to DateTime and combine them into a single 'DateTime' column
df['DateTime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Extract date of today
today_date = datetime.now().strftime("%Y-%m-%d")

# Get the first date in the dataset
first_date = df['DateTime'].min().strftime("%Y-%m-%d")

# Filter data for Zone B and Zone C
zone_b_data = df[['DateTime', 'Zone B subzone 1', 'Zone B subzone 2', 'Mean zone B']]
zone_c_data = df[['DateTime', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone C']]

# Plotting Zone B data
plt.figure(figsize=(10, 6))
plt.plot(zone_b_data['DateTime'], zone_b_data['Zone B subzone 1'], label='Zone B Subzone1')
plt.plot(zone_b_data['DateTime'], zone_b_data['Zone B subzone 2'], label='Zone B Subzone2')
plt.plot(zone_b_data['DateTime'], zone_b_data['Mean zone B'], label='Zone B Mean')

plt.title('Temperature Zone B - {} to {}'.format(first_date, today_date))
plt.xlabel('DateTime')
plt.ylabel('Temperature (C)')
plt.legend()
plt.grid(True)
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Temp\Temp_zone_b_{}_to_{}.svg".format(first_date, today_date))
plt.show()

# Plotting Zone C data
plt.figure(figsize=(10, 6))
plt.plot(zone_c_data['DateTime'], zone_c_data['Zone C subzone 1'], label='Zone C Subzone1')
plt.plot(zone_c_data['DateTime'], zone_c_data['Zone C subzone 2'], label='Zone C Subzone2')
plt.plot(zone_c_data['DateTime'], zone_c_data['Mean zone C'], label='Zone C Mean')

plt.title('Temperature Zone C - {} to {}'.format(first_date, today_date))
plt.xlabel('DateTime')
plt.ylabel('Temperature (C)')
plt.legend()
plt.grid(True)
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\Temp\Temp_zone_c_{}_to_{}.svg".format(first_date, today_date))
plt.show()

