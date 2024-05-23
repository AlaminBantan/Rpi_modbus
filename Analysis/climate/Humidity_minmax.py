import pandas as pd

# Read the CSV file
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Humidity_data.csv"
df = pd.read_csv(file_path)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Extract the day from the datetime
df['day'] = df['date'].dt.date

# Group by day and calculate max, min, and mean for 'Mean zone B' and 'Mean zone C'
result = df.groupby('day').agg({
    'Mean zone B': ['max', 'min', 'mean'],
    'Mean zone C': ['max', 'min', 'mean']
})

# Print the result
print(result)

