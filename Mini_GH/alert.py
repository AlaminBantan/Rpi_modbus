import pandas as pd
import yagmail
from datetime import datetime
import time

# Define a function to check temperature and send email if condition is met
def check_temperature_and_send_alert():
    # Read the CSV file
    df = pd.read_csv("/home/cdacea/south_GH/south_climate.csv")

    # Convert 'datetime' column to datetime format and set it as the index
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # Convert non-numeric values to NaN and replace negative values with zero
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.round(2)
    df[df < 0] = 0

    # Check if any temperature exceeds 27C in the latest data
    over_temp = df[df['Temperature_south (c)'] > 27]

    # If there's any temperature over 27°C, send the alert email
    if not over_temp.empty:
        # Set up your yagmail instance
        email_address = '-'  # Your email address
        password = '-'  # Your email password
        yag = yagmail.SMTP(email_address, password)

        try:
            # Compose the email
            to = ['-']  # Your recipient email address
            
            # Generate today's date
            today_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            
            # Update the subject with today's date
            subject = f'ALERT: South Greenhouse Temperature Exceeded 27°C at {today_date}'
            
            body = f"Attention: The temperature in the South Greenhouse exceeded 27°C at {today_date}. Please check the conditions."

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
    check_temperature_and_send_alert()
    # Sleep for 15 minutes (900 seconds)
    time.sleep(900)
