import pandas as pd

# Read the CSV file
file_path = r"C:\Users\bantanam\KAUST\CDA-CEA Team - Documents\CO2 misting - Cucumber trial\Data collection\Climatic_data\mean_PAR_data.csv"
df = pd.read_csv(file_path)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Group by date and calculate DLI for Mean Zone B and Mean Zone C
daily_dli = df.groupby('date').apply(lambda group: (group['Mean zone B'].sum() * 15 * 60 / 1000000, group['Mean zone C'].sum() * 15 * 60 / 1000000))

# Print the results
for date, (mean_zone_b_dli, mean_zone_c_dli) in daily_dli.items():
    print(f"DLI for Mean Zone B on {date.date()}: {mean_zone_b_dli:.2f} mol/m^2")
    print(f"DLI for Mean Zone C on {date.date()}: {mean_zone_c_dli:.2f} mol/m^2")

    print()
