import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file
csv_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_CO2Conc_data.csv"
df = pd.read_csv(csv_path)

# Convert 'date' and 'time' columns to datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Group by hour and calculate the mean for Zone B subzone 1 and Zone C subzone 1
hourly_mean = df.groupby(df['datetime'].dt.hour)[['Zone B subzone 1', 'Zone C subzone 1']].mean()

# Output folder for saving SVG plots
output_folder = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\CO2 conc"

# Ensure the output folder exists, create it if not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Plotting for Zone B subzone 1
plt.figure(figsize=(10, 6))
hourly_mean['Zone B subzone 1'].plot(label='Zone B')
plt.title('Average CO2 Concentration for Zone B')
plt.xlabel('Hour')
plt.ylabel('CO2 Concentration')
plt.ylim(350, 450)
plt.legend()

# Save the plot as SVG
plt.savefig(os.path.join(output_folder, 'average_co2_zone_b.svg'))
plt.close()

# Plotting for Zone C subzone 1
plt.figure(figsize=(10, 6))
hourly_mean['Zone C subzone 1'].plot(label='Zone C', color='green')
plt.title('Average CO2 Concentration for Zone C')
plt.xlabel('Hour')
plt.ylabel('CO2 Concentration')
plt.ylim(350, 450)
plt.legend()

# Save the plot as SVG
plt.savefig(os.path.join(output_folder, 'average_co2_zone_c.svg'))
plt.show()
plt.close()
