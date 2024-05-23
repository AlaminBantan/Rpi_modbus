import subprocess

scripts = [
    "CO2_conc_plots.py",
    "Humidity_plots.py",
    "PAR_plots.py",
    "Temp_plots.py",
    "Solar_plots.py"
]

folder_path = r"C:\Users\bantanam\Desktop\Rpi-modbus\Analysis\climate"

processes = [subprocess.Popen(["python", script], cwd=folder_path) for script in scripts]

for process in processes:
    process.wait()
