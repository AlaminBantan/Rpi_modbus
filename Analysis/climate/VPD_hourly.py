import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the CSV file
csv_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_VPD_data.csv"
df = pd.read_csv(csv_path)

# Convert 'date' and 'time' columns to datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Group by hour and calculate the mean for Mean zone B and Mean zone C
hourly_mean = df.groupby(df['datetime'].dt.hour)[['Mean zone B', 'Mean zone C']].mean()

# Output folder for saving SVG plots
output_folder = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\plots\VPD"

# Ensure the output folder exists, create it if not
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Plotting for Mean zone B
plt.figure(figsize=(10, 6))
hourly_mean['Mean zone B'].plot(label='Mean zone B')
plt.title('Average VPD for Zone B by Hour')
plt.xlabel('Hour')
plt.ylabel('VPD')
plt.legend()

# Save the plot as SVG
plt.savefig(os.path.join(output_folder, 'average_vpd_zone_b.svg'))
plt.close()

# Plotting for Mean zone C
plt.figure(figsize=(10, 6))
hourly_mean['Mean zone C'].plot(label='Mean zone C', color='green')
plt.title('Average VPD for Zone C by Hour')
plt.xlabel('Hour')
plt.ylabel('VPD')
plt.legend()

# Save the plot as SVG
plt.savefig(os.path.join(output_folder, 'average_vpd_zone_c.svg'))
plt.close()
