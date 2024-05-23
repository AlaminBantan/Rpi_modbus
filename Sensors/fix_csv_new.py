import pandas as pd

# Assuming 'C:\\Users\\bantanam\\Downloads\\Light_comparison.csv' is the file containing your data
df = pd.read_csv('C:\\Users\\bantanam\\Downloads\\Light_comparison.csv')

# Convert 'Date' and 'Time' columns to datetime format
df['Date'] = pd.to_datetime(df['Date'])
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time

# Create separate columns for date and time
df['Date'] = df['Date'].dt.date
df['Time'] = df['Time'].apply(lambda x: x.strftime('%H:%M'))

# Replace negative values with 0 in specific columns
cols_to_replace = ['PAR Intensity Zone B (1)', 'PAR Intensity Zone C (1)', 'Solar Radiation Zone B (1)', 'Solar Radiation Zone C (1)', 'PAR Intensity Zone B (2)', 'PAR Intensity Zone C (2)', 'Solar Radiation Zone B (2)', 'Solar Radiation Zone C (2)', 'PAR Intensity Zone B (3)', 'PAR Intensity Zone C (3)', 'Solar Radiation Zone B (3)', 'Solar Radiation Zone C (3)']
df[cols_to_replace] = df[cols_to_replace].apply(lambda x: x.clip(lower=0))

# Combine 'Date' and 'Time' to a single datetime column
df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))

# Set 'Datetime' as the index
df.set_index('Datetime', inplace=True)

# Resample the data to 15-minute intervals and calculate the mean
df_15min = df.resample('15T').mean()

# Reorder the columns
desired_order = ['PAR Intensity Zone B (1)', 'PAR Intensity Zone B (2)', 'PAR Intensity Zone B (3)', 'PAR Intensity Zone C (1)', 'PAR Intensity Zone C (2)',  'PAR Intensity Zone C (3)', 'Solar Radiation Zone B (1)', 'Solar Radiation Zone B (2)', 'Solar Radiation Zone B (3)', 'Solar Radiation Zone C (1)' ,'Solar Radiation Zone C (2)', 'Solar Radiation Zone C (3)']

                  
                 
df_15min = df_15min[desired_order]


# Reset the index to get the 'Datetime' column back
df_15min.reset_index(inplace=True)

# Extract separate columns for date and time
df_15min['Date'] = df_15min['Datetime'].dt.date
df_15min['Time'] = df_15min['Datetime'].dt.time

# Save the consolidated data as a CSV file
df_15min.to_csv('C:\\Users\\bantanam\\Downloads\\updated_Light_comparison_15min.csv', index=False)
