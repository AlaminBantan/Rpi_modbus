import pandas as pd
import numpy as np
import yagmail
import os
from datetime import datetime

SRC = "/home/cdacea/climate/Zone1_minute.csv"
DST = "/home/cdacea/climate/Zone1_15min.csv"

# --- Load ---
df = pd.read_csv(SRC)

# Ensure datetime is parsed and used as index
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df = df.dropna(subset=['datetime']).set_index('datetime').sort_index()

# Convert all non-datetime columns to numeric where possible
for col in df.columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Optional: clamp negatives to 0 for inherently non-negative metrics
# (keep temperature and dew point as-is)
non_negative_cols = [c for c in df.columns if any(
    key in c for key in ["PAR", "RH", "CO2", "Pressure", "VPD", "FanRPM"]
)]
df[non_negative_cols] = df[non_negative_cols].clip(lower=0)

# 15-minute resample (labelled at the bin end by default)
result = df.resample('15min').mean()

# Round to 2 decimals
result = result.round(2)

# Save
os.makedirs(os.path.dirname(DST), exist_ok=True)
result.to_csv(DST)

# --- Email via yagmail ---
# Use an app password for Gmail (recommended).
EMAIL_ADDR = "your_email@example.com"
EMAIL_PASS = "your_app_password_here"   # e.g., Gmail App Password
RECIPIENTS = ["recipient1@example.com"] # add more as needed

yag = yagmail.SMTP(EMAIL_ADDR, EMAIL_PASS)

try:
    today_date = datetime.now().strftime('%Y-%m-%d')
    subject = f'Zone1 Climate (15-min averages): {today_date}'
    body = f'Attached are the 15-minute averages for Zone1 on {today_date}.'

    yag.send(to=RECIPIENTS, subject=subject, contents=[body, DST])
    print("Email sent successfully!")

except Exception as e:
    print(f"Error sending email: {e}")

finally:
    try:
        yag.close()
    except Exception:
        pass
