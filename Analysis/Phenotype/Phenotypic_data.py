import subprocess

scripts = [
    "Stem elongation both zones.py",
    "5th leaf both zones.py",
    "5th leaf width both zones.py",
    "5th leaf length both zones.py",
    "10th leaf both zones.py",
    "10th leaf length both zones.py",
    "10th leaf width both zones.py"

]

folder_path = r"C:\Users\bantanam\Desktop\Rpi-modbus\Analysis\Phenotype"

processes = [subprocess.Popen(["python", script], cwd=folder_path) for script in scripts]

for process in processes:
    process.wait()
