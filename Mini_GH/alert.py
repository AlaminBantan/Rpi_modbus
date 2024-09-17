import pandas as pd
import yagmail
from datetime import datetime
import time

# Define a function to check the latest temperature and send an alert if condition is met
def check_latest_temperature_and_send_alert():
    # Read the CSV file
    df = pd.read_csv("/home/cdacea/south_GH/south_climate.csv")

    # Print the column names to ensure the correct column is being accessed
    print(f"Columns in the CSV: {df.columns}")

    # Convert 'datetime' column to datetime format and set it as the index
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # Convert non-numeric values to NaN and replace negative values with zero
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.round(2)
    df[df < 0] = 0

    # Get the latest temperature value
    temp_column = 'Temperature_south (c)'  # Ensure this matches exactly with your CSV file
    latest_temp = df[temp_column].iloc[-1]  # Get the latest temperature reading

    # Debug: print the latest temperature being checked
    print(f"Latest temperature: {latest_temp}")

    # Check if the latest temperature exceeds 27°C
    if latest_temp > 27:
        # Set up your yagmail instance
        email_address = '-'  # Your email address
        password = '-'  # Your email password
        yag = yagmail.SMTP(email_address, password)

        try:
            # Compose the email
            to = ['-']  # Your recipient email address
            
            # Generate today's date and time
            today_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            # Update the subject with today's date
            subject = f'ALERT: South Greenhouse Temperature Exceeded 27°C at {today_date}'
            
            body = f"Attention: The temperature in the South Greenhouse exceeded 27°C at {today_date}. The latest temperature recorded is {latest_temp}°C."

            # Send the email (without attachment)
            yag.send(to, subject, body)

            # Log success or other relevant information
            print("Temperature alert email sent successfully!")

        except Exception as e:
            # Log the error
            print(f"Error: {e}")

        finally:
            # Logout
            yag.close()

    else:
        print("No temperature alerts at this time.")


# Loop that runs the check every 15 minutes
while True:
    check_latest_temperature_and_send_alert()
    # Sleep for 15 minutes (900 seconds)
    time.sleep(900)
