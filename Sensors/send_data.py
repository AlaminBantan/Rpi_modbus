import yagmail
from datetime import datetime

# Set up your yagmail instance
email_address = 'bantanalamin@gmail.com'
password = 'muzomvmpwxiczzmo'
yag = yagmail.SMTP(email_address, password)

try:
    # Compose the email
    to = ['alamin.bantan@kaust.edu.sa']
    
    # Generate today's date
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    # Update the subject with today's date
    subject = f'Climatic of the zones: {today_date}'
    
    body = f'These are the climatic data from zones b and c until {today_date}'

    # Attach the file
    attachment1 = "/home/cdacea/GH_data/modified_data_15min.csv"

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
