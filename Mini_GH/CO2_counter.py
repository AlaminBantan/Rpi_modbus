import re
from collections import defaultdict

# Initialize a dictionary to store the counts
relay_on_count = defaultdict(int)

# Define the log file name and output file name
log_file = 'relay_control_all.log'
output_file = 'relay_on_counts.txt'

# Define the regex pattern to capture the date and relay ON message
pattern = re.compile(r'(\d{4}-\d{2}-\d{2}) .*Relay turned ON')

# Read the log file
with open(log_file, 'r') as file:
    for line in file:
        match = pattern.search(line)
        if match:
            # Extract the date and increment the counter for that date
            date = match.group(1)
            relay_on_count[date] += 1

# Write the result to the output file
with open(output_file, 'w') as out_file:
    for day, count in relay_on_count.items():
        out_file.write(f"Day: {day} - Number of times relay was ON: {count}\n")

print(f"Relay ON counts saved to {output_file}")
