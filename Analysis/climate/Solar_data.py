import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\modified_data_15min.csv')

# Extract relevant columns
df_extracted = df[['RoundedDateTime', 'Zone', 'Subzone', 'Solar radiation']]

# Pivot the table to have zones and subzones as columns
df_pivoted = df_extracted.pivot_table(index=['RoundedDateTime'], columns=['Zone', 'Subzone'], values='Solar radiation')

# Calculate mean values for each zone
df_pivoted['Mean zone B'] = (df_pivoted[('B', 1)] + df_pivoted[('B', 2)]) / 2
df_pivoted['Mean zone C'] = (df_pivoted[('C', 1)] + df_pivoted[('C', 2)]) / 2

# Replace negative values with 0
df_pivoted[df_pivoted < 0] = 0

# Round numbers to 2 decimal places
df_pivoted = df_pivoted.round(2)

# Reset the index to have 'date' as a separate column
df_pivoted.reset_index(inplace=True)
df_pivoted.columns = ['date', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']

# Split 'date' column into 'date' and 'time'
df_pivoted[['date', 'time']] = df_pivoted['date'].str.split(expand=True)

# Rearrange columns to have 'time' next to 'date'
df_pivoted = df_pivoted[['date', 'time', 'Zone B subzone 1', 'Zone B subzone 2', 'Zone C subzone 1', 'Zone C subzone 2', 'Mean zone B', 'Mean zone C']]

# Save the result to a new CSV file
df_pivoted.to_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\mean_SolarRadiation_data.csv', index=False)

