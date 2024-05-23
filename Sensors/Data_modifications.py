import pandas as pd

# Load the CSV file into a DataFrame
file_path = "/home/cdacea/GH_data/climatic_data.csv"
df = pd.read_csv(file_path)

# Convert the 'Date' and 'Time' columns to datetime format
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Convert 'CO2 conc' column to numeric, ignoring errors to handle non-numeric values
df['CO2 conc'] = pd.to_numeric(df['CO2 conc'], errors='coerce')

# Round the 'DateTime' column to the nearest 15-minute interval
df['RoundedDateTime'] = df['DateTime'].dt.round('15min')

# Group by 'RoundedDateTime', 'Zone', and 'Subzone' and calculate the mean for each group
grouped_data = df.groupby(['RoundedDateTime', 'Zone', 'Subzone']).mean(numeric_only=True).reset_index()

# Save the grouped data to a new CSV file in the same directory
output_file_path = "/home/cdacea/GH_data/modified_data_15min.csv"
grouped_data.to_csv(output_file_path, index=False)

# Print the result
print(f"Grouped and averaged data for 15-minute intervals saved to {output_file_path}")
