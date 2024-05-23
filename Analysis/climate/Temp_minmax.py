import pandas as pd

# Read the CSV file
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_Temperature_data.csv"
df = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Group by date and calculate the minimum, maximum, and mean for Mean Zone B and Mean Zone C
result = df.groupby(df['date'].dt.date).agg({
    'Mean zone B': ['min', 'max', 'mean'],
    'Mean zone C': ['min', 'max', 'mean']
}).reset_index()

# Rename the columns for better readability
result.columns = ['Date', 'Min Zone B', 'Max Zone B', 'Avg Zone B', 'Min Zone C', 'Max Zone C', 'Avg Zone C']

# Print the result
print(result)

