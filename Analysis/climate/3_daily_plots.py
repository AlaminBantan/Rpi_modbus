import subprocess

scripts = [
    "CO2_conc_daily.py",
    "Humidity_daily.py",
    "PAR_daily.py",
    "Temp_daily.py",
    "Solar_daily.py"
]

folder_path = r"C:\Users\bantanam\Desktop\Rpi-modbus\Analysis\climate"

processes = [subprocess.Popen(["python", script], cwd=folder_path) for script in scripts]

for process in processes:
    process.wait()
