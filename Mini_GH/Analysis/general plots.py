import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




# Read CSV files
df_north = pd.read_csv(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\north_modified.csv")
df_south = pd.read_csv(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\south_modified.csv")

# Convert 'datetime' column to datetime type
df_north['datetime'] = pd.to_datetime(df_north['datetime'])
df_south['datetime'] = pd.to_datetime(df_south['datetime'])

# Calculate DLI (Daily Light Integral) for North and South greenhouses
df_north['date'] = df_north['datetime'].dt.date
df_south['date'] = df_south['datetime'].dt.date

dli_north = df_north.groupby('date')['PAR_north (umol.m-1.s-1)'].sum() * 15 * 60 / 1000000  # Calculate DLI for North greenhouse
dli_south = df_south.groupby('date')['PAR_south (umol.m-1.s-1)'].sum() * 15 * 60 / 1000000  # Calculate DLI for South greenhouse

# Plotting DLI Comparison
plt.figure(figsize=(10, 6))
plt.plot(dli_north.index, dli_north, color='red', label='North Greenhouse')
plt.plot(dli_south.index, dli_south, color='blue', label='South Greenhouse')
plt.xlabel('Date')
plt.ylabel('DLI (mol/m²/day)')
plt.title('DLI Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\DLI_Comparison.png")
plt.show()




# Plotting PAR 
plt.figure(figsize=(10, 6))
plt.plot(df_north['datetime'], df_north['PAR_north (umol.m-1.s-1)'], color='red', label='North Greenhouse')
plt.plot(df_south['datetime'], df_south['PAR_south (umol.m-1.s-1)'], color='blue', label='South Greenhouse')
plt.xlabel('Time')
plt.ylabel('PAR (umol.m-1.s-1)')
plt.title('PAR Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\PAR_Comparison.png")
plt.show()


# Plotting Solar Radiation
plt.figure(figsize=(10, 6))
plt.plot(df_north['datetime'], df_north['Solar radiation_north (w.m-2)'], color='red', label='North Greenhouse')
plt.plot(df_south['datetime'], df_south['Solar radiation_south (w.m-2)'], color='blue', label='South Greenhouse')
plt.xlabel('Time')
plt.ylabel('Solar Radiation (w.m-2)')
plt.title('Solar Radiation Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\SolarRadiation_Comparison.png")
plt.show()

# Plotting Temperature
plt.figure(figsize=(10, 6))
plt.plot(df_north['datetime'], df_north['Temperature_north (c)'], color='red', label='North Greenhouse')
plt.plot(df_south['datetime'], df_south['Temperature_south (c)'], color='blue', label='South Greenhouse')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.ylim((10,50))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\Temperature_Comparison.png")
plt.show()

# Plotting Humidity
plt.figure(figsize=(10, 6))
plt.plot(df_north['datetime'], df_north['Humidity_north (%)'], color='red', label='North Greenhouse')
plt.plot(df_south['datetime'], df_south['Humidity_south (%)'], color='blue', label='South Greenhouse')
plt.xlabel('Time')
plt.ylabel('Humidity (%)')
plt.title('Humidity Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.ylim((0,100))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\Humidity_Comparison.png")
plt.show()


# Plotting CO2 Concentration
plt.figure(figsize=(10, 6))
plt.plot(df_north['datetime'], df_north['CO2 conc_north (ppm)'], color='red', label='North Greenhouse')
plt.plot(df_south['datetime'], df_south['CO2 conc_south (ppm)'], color='blue', label='South Greenhouse')
plt.xlabel('Time')
plt.ylabel('CO2 Concentration (ppm)')
plt.title('CO2 Concentration Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\CO2Concentration_Comparison.png")
plt.show()


# Calculate Absolute Humidity
def calculate_absolute_humidity(temperature, relative_humidity):
    # Constants for the Magnus formula
    a = 6.112  # mbar
    b = 17.67
    c = 243.5  # °C

    # Calculate saturation vapor pressure
    svp = a * np.exp((b * temperature) / (c + temperature))

    # Calculate actual vapor pressure
    avp = (relative_humidity / 100) * svp

    # Calculate absolute humidity
    absolute_humidity = (217 * avp) / (temperature + 273.15)
    return absolute_humidity

# Add Absolute Humidity to DataFrames
df_north['Absolute Humidity_north (g/m³)'] = calculate_absolute_humidity(df_north['Temperature_north (c)'], df_north['Humidity_north (%)'])
df_south['Absolute Humidity_south (g/m³)'] = calculate_absolute_humidity(df_south['Temperature_south (c)'], df_south['Humidity_south (%)'])

# Plotting Absolute Humidity
plt.figure(figsize=(10, 6))
plt.plot(df_north['datetime'], df_north['Absolute Humidity_north (g/m³)'], color='red', label='North Greenhouse')
plt.plot(df_south['datetime'], df_south['Absolute Humidity_south (g/m³)'], color='blue', label='South Greenhouse')
plt.xlabel('Time')
plt.ylabel('Absolute Humidity (g/m³)')
plt.title('Absolute Humidity Comparison')
plt.legend(loc='upper right', bbox_to_anchor=(1.3,1))
plt.grid(True)
plt.tight_layout()
plt.savefig(r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\MiniGH_experiments\climatic data\AbsoluteHumidity_Comparison.png")
plt.show()