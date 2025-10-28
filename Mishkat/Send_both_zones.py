#!/usr/bin/env python3
import os
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# ====== CONFIG ======
CSV_DIR = "/home/cdacea/climate"
SRC1 = os.path.join(CSV_DIR, "Zone1_minute.csv")
SRC3 = os.path.join(CSV_DIR, "Zone3_minute.csv")
DST1 = os.path.join(CSV_DIR, "Zone1_15min.csv")
DST3 = os.path.join(CSV_DIR, "Zone3_15min.csv")
ACTIONS = os.path.join(CSV_DIR, "mist_actions.csv")

EMAIL_ADDR = "alaminbantan2@gmail.com"
EMAIL_PASS = os.environ.get("MAIL_APP_PASSWORD", "")  # set securely
RECIPIENTS = ["alamin.bantan@kaust.edu.sa", "chad.vietti@kaust.edu.sa"]

KSA = ZoneInfo("Asia/Riyadh")

# ====== Helpers ======
def process_zone(src, dst, zone_label):
    """Load minute CSV, average to 15-min means over all available data."""
    if not os.path.exists(src):
        print(f"[WARN] Missing {src}")
        return None

    # Read safely (remove NULs if any)
    with open(src, "rb") as fb:
        raw = fb.read().replace(b"\x00", b"")
    from io import BytesIO
    df = pd.read_csv(BytesIO(raw))

    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
    df = df.dropna(subset=["datetime"]).set_index("datetime").sort_index()
    df.index = df.index.tz_convert(KSA)

    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Clamp negatives for metrics that must be ≥0
    nonneg_keys = ["PAR", "RH", "CO2", "Pressure", "VPD", "FanRPM", "PlantVPD"]
    nonneg_cols = [c for c in df.columns if any(k in c for k in nonneg_keys)]
    df[nonneg_cols] = df[nonneg_cols].clip(lower=0)

    # Resample over all time
    out = df.resample("15min").mean().round(2)
    out.to_csv(dst)
    print(f"[OK] {zone_label} → {dst}")
    print(f"  Span: {out.index.min()} → {out.index.max()} ({len(out)} rows)")
    return dst

# ====== Process both zones ======
f1 = process_zone(SRC1, DST1, "Zone1")
f3 = process_zone(SRC3, DST3, "Zone3")

# ====== Mist actions (all history) ======
act_file = None
if os.path.exists(ACTIONS) and os.path.getsize(ACTIONS) > 0:
    act = pd.read_csv(ACTIONS)
    act["datetime_utc"] = pd.to_datetime(act["datetime_utc"], errors="coerce", utc=True)
    act = act.dropna(subset=["datetime_utc"])
    act["datetime_ksa"] = act["datetime_utc"].dt.tz_convert(KSA)
    act = act.sort_values("datetime_ksa")
    act_file = ACTIONS  # use the full file
    print(f"[OK] Included all mist actions ({len(act)} records)")

# ====== Email all three ======
try:
    import yagmail
except ImportError:
    raise SystemExit("Please install yagmail first: pip install yagmail")

if not EMAIL_PASS:
    raise SystemExit("Missing MAIL_APP_PASSWORD env var for Gmail app password.")

yag = yagmail.SMTP(EMAIL_ADDR, EMAIL_PASS)

subject = "Mishkat Climate Report — Full Historical Data"
body = (
    "This report includes all available data since logging began.\n\n"
    "Attached files:\n"
    f" • Zone1 15-min averages ({os.path.basename(DST1)})\n"
    f" • Zone3 15-min averages ({os.path.basename(DST3)})\n"
    f" • Full misting log ({os.path.basename(ACTIONS)})\n\n"
    "Notes:\n"
    " - ‘PlantTemp’ = Air Temp − 2 °C\n"
    " - ‘PlantVPD’ recalculated from PlantTemp and RH\n"
)

attachments = [p for p in [DST1, DST3, act_file] if p and os.path.exists(p) and os.path.getsize(p) > 0]

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
