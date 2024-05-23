import pandas as pd
import math

# Read temperature data from CSV
temp_df = pd.read_csv(r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Temperature_data.csv')
# Assuming the temperature is in columns 'Mean zone B' and 'Mean zone C'
temperature_b = temp_df['Mean zone B']
temperature_c = temp_df['Mean zone C']

# Read humidity data from CSV
humidity_df = pd.read_csv(r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Humidity_data.csv')
# Assuming humidity is in columns 'Mean zone B' and 'Mean zone C'
humidity_b = humidity_df['Mean zone B']
humidity_c = humidity_df['Mean zone C']

# Constants for temperature in Celsius
A = 0.61078
B = 17.2694
C = 273.3

# Calculate saturation vapor pressure (es)
def calculate_es(temp):
    return A * math.exp((B * temp) / (temp + C))

# Calculate actual vapor pressure (ea)
def calculate_ea(temp, hum):
    es = calculate_es(temp)
    return (hum / 100) * es

# Calculate VPD for Mean zone B
def calculate_vpd_b(temp, hum):
    es = calculate_es(temp)
    ea = calculate_ea(temp, hum)
    return es - ea

# Calculate VPD for Mean zone C
def calculate_vpd_c(temp, hum):
    es = calculate_es(temp)
    ea = calculate_ea(temp, hum)
    return es - ea

# Calculate and add new columns for VPD in the temperature dataframe
temp_df['Mean zone B'] = [calculate_vpd_b(temp, hum) for temp, hum in zip(temperature_b, humidity_b)]
temp_df['Mean zone C'] = [calculate_vpd_c(temp, hum) for temp, hum in zip(temperature_c, humidity_c)]

# Save the result to a new CSV file in the specified directory
result_path = r'C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_VPD_data.csv'
temp_df[['date', 'time', 'Mean zone B', 'Mean zone C']].to_csv(result_path, index=False)
