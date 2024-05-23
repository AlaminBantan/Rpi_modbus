import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\modified_data_15min.csv')

# Extract relevant columns
df_extracted = df[['RoundedDateTime', 'Zone', 'Subzone', 'CO2 conc']]

# Pivot the table to have zones and subzones as columns
df_pivoted = df_extracted.pivot_table(index=['RoundedDateTime'], columns=['Zone', 'Subzone'], values='CO2 conc')


# Replace negative values with 0
df_pivoted[df_pivoted < 0] = 0

# Round numbers to 2 decimal places
df_pivoted = df_pivoted.round(2)

# Reset the index to have 'date' as a separate column
df_pivoted.reset_index(inplace=True)
df_pivoted.columns = ['date', 'Zone B subzone 1', 'Zone C subzone 1']

# Split 'date' column into 'date' and 'time'
df_pivoted[['date', 'time']] = df_pivoted['date'].str.split(expand=True)

# Rearrange columns to have 'time' next to 'date'
df_pivoted = df_pivoted[['date', 'time', 'Zone B subzone 1',  'Zone C subzone 1']]

# Save the result to a new CSV file
df_pivoted.to_csv('C:\\Users\\bantanam\\KAUST\\CDA-CEA Team - Documents\\CO2 misting - Cucumber trial\\Data collection\\Climatic_data\\mean_CO2Conc_data.csv', index=False)

