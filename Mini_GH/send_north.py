import pandas as pd
import numpy as np
import yagmail
from datetime import datetime

# Read the CSV file
df = pd.read_csv("/home/cdacea/north_GH/north_climate.csv")

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
modified_file_path = "/home/cdacea/north_GH/north_modified.csv"
result.to_csv(modified_file_path)

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
    subject = f'Climatic of the north_GH: {today_date}'
    
    body = f'These are the climatic data from north_GH {today_date}'

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
