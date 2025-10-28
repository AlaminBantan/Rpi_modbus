#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# ====== CONFIG ======
CSV_DIR = "/home/cdacea/climate"
SRC1 = os.path.join(CSV_DIR, "Zone1_minute.csv")
SRC3 = os.path.join(CSV_DIR, "Zone3_minute.csv")
DST1 = os.path.join(CSV_DIR, "Zone1_15min.csv")
DST3 = os.path.join(CSV_DIR, "Zone3_15min.csv")
ACTIONS = os.path.join(CSV_DIR, "mist_actions.csv")
ACTIONS_D = os.path.join(CSV_DIR, "mist_actions_daily.csv")

EMAIL_ADDR = "alaminbantan2@gmail.com"
EMAIL_PASS = os.environ.get("MAIL_APP_PASSWORD", "")  # set securely
RECIPIENTS = ["alamin.bantan@kaust.edu.sa", "chad.vietti@kaust.edu.sa"]

KSA = ZoneInfo("Asia/Riyadh")

# ====== Determine greenhouse day (03:00 → 03:00) ======
now_ksa = datetime.now(KSA)
day_end = now_ksa.replace(hour=3, minute=0, second=0, microsecond=0)
if now_ksa.hour < 3:
    day_end -= timedelta(days=1)
day_start = day_end - timedelta(days=1)

def process_zone(src, dst, zone_label):
    """Load minute CSV, slice greenhouse day, average to 15-min means."""
    if not os.path.exists(src):
        print(f"[WARN] Missing {src}")
        return None
    df = pd.read_csv(src)
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
    df = df.dropna(subset=["datetime"]).set_index("datetime").sort_index()
    df.index = df.index.tz_convert(KSA)

    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Clamp negatives for metrics that must be ≥0
    nonneg_keys = ["PAR", "RH", "CO2", "Pressure", "VPD", "FanRPM", "PlantVPD"]
    nonneg_cols = [c for c in df.columns if any(k in c for k in nonneg_keys)]
    df[nonneg_cols] = df[nonneg_cols].clip(lower=0)

    # Slice current greenhouse day
    win = df.loc[(df.index >= day_start) & (df.index < day_end)]
    if win.empty:
        print(f"[WARN] No data for {zone_label} in this period")
        return None

    # 15-min average
    out = win.resample("15min").mean().round(2)
    out.to_csv(dst)
    print(f"[OK] {zone_label} → {dst}")
    return dst

# ====== Process both zones ======
f1 = process_zone(SRC1, DST1, "Zone1")
f3 = process_zone(SRC3, DST3, "Zone3")

# ====== Filter mist actions ======
act_day = None
if os.path.exists(ACTIONS) and os.path.getsize(ACTIONS) > 0:
    act = pd.read_csv(ACTIONS)
    act["datetime_utc"] = pd.to_datetime(act["datetime_utc"], errors="coerce", utc=True)
    act = act.dropna(subset=["datetime_utc"])
    act["datetime_ksa"] = act["datetime_utc"].dt.tz_convert(KSA)
    mask = (act["datetime_ksa"] >= day_start) & (act["datetime_ksa"] < day_end)
    act_day = act.loc[mask]
    if not act_day.empty:
        act_day.to_csv(ACTIONS_D, index=False)
        print(f"[OK] Filtered mist actions → {ACTIONS_D}")
    else:
        print("[WARN] No mist actions in this period")

# ====== Email all three ======
try:
    import yagmail
except ImportError:
    raise SystemExit("Please install yagmail first: pip install yagmail")

if not EMAIL_PASS:
    raise SystemExit("Missing MAIL_APP_PASSWORD env var for Gmail app password.")

yag = yagmail.SMTP(EMAIL_ADDR, EMAIL_PASS)

label_date = day_start.date().isoformat()
subject = f"Mishkat Climate Daily Report — {label_date}"
body = (
    f"Time window (KSA): {day_start.strftime('%Y-%m-%d %H:%M')} → {day_end.strftime('%Y-%m-%d %H:%M')}\n\n"
    "Attached files:\n"
    f" • Zone1 15-min averages ({os.path.basename(DST1)})\n"
    f" • Zone3 15-min averages ({os.path.basename(DST3)})\n"
    f" • Misting actions ({os.path.basename(ACTIONS_D) if act_day is not None else '(none found)'})\n\n"
    "Notes:\n"
    " - ‘PlantTemp’ = Air Temp − 2 °C\n"
    " - ‘PlantVPD’ recalculated from PlantTemp and RH\n"
)

attachments = [p for p in [DST1, DST3, ACTIONS_D] if p and os.path.exists(p) and os.path.getsize(p) > 0]

try:
    yag.send(to=RECIPIENTS, subject=subject, contents=[body] + attachments)
    print("✅ Email sent successfully.")
except Exception as e:
    print(f"❌ Error sending email: {e}")
finally:
    try:
        yag.close()
    except Exception:
        pass
