import pandas as pd

# Read the CSV file
df = pd.read_csv("/home/cdacea/north_GH/north_climate.csv")

# Convert 'datetime' column to datetime format
df['datetime'] = pd.to_datetime(df['datetime'])

# Set 'datetime' column as the index
df.set_index('datetime', inplace=True)

# Group by datetime for each minute and average every 15 minutes
result = df.resample('15T').mean()

print(result)
