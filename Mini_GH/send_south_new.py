import pandas as pd
import yagmail
from datetime import datetime
import re
from collections import defaultdict

# Function to count the number of times the CO2 relay was ON from a start date to today
def count_relay_on_from_date(log_file, start_date):
    relay_on_count = defaultdict(int)
    pattern = re.compile(r'(\d{4}-\d{2}-\d{2}) .*Relay turned ON')

    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                date = match.group(1)
                if date >= start_date:
                    relay_on_count[date] += 1

    return relay_on_count

# Define the start date
start_date = '2024-09-18'  # Adjust this date as needed

# Read the CSV file
df = pd.read_csv("/home/cdacea/south_GH/south_climate.csv")

# Convert 'datetime' column to datetime format and set it as the index
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)

# Convert non-numeric values to NaN
df = df.apply(pd.to_numeric, errors='coerce')

# Round all values to two decimal places
df = df.round(2)

# Replace negative values with zero
df[df < 0] = 0

# Group by datetime for each minute and average every 15 minutes
result = df.resample('15min').mean()

# Round all values to two decimal places
result = result.round(2)

# Save the result to CSV
modified_file_path = "/home/cdacea/south_GH/south_modified.csv"
result.to_csv(modified_file_path)

# Count CO2 relay ON occurrences from the start date
log_file = 'relay_control_all.log'
relay_on_counts = count_relay_on_from_date(log_file, start_date)

# Set up your yagmail instance
email_address = '-'
password = '-'
yag = yagmail.SMTP(email_address, password)

try:
    # Compose the email
    to = [-]
    
    # Generate today's date
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Update the subject with today's date
    subject = f'Climatic data of the south_GH: {today_date}'
    
    # Create the email body with relay counts
    body = (f'These are the climatic data from south_GH {today_date}\n\n'
            f'CO2 Enrichment Relay Counts from {start_date} to {today_date}:\n')
    
    for date, count in sorted(relay_on_counts.items()):
        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d %b')  # Format date as '18 Sep'
        body += f'{formatted_date}: {count} times\n'

    # Attach the modified file
    attachment1 = modified_file_path

    # Send the email
    yag.send(to, subject, [body, attachment1])

    # Log success or other relevant information
    print("Email sent successfully!")

except Exception as e:
    # Log the error
    print(f"Error: {e}")

finally:
    # Logout
    yag.close()
