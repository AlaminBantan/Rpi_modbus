import csv

# Input file path
file_path = '/home/cdacea/GH_data/climatic_data.csv'

# Read the CSV file and remove duplicate headers
with open(file_path, 'r+', newline='') as file:
    reader = csv.reader(file)
    writer = csv.writer(file)

    # Flag to skip the first header
    skip_header = True

    # Store the lines to rewrite the file if needed
    lines_to_write = []

    for row in reader:
        if not skip_header:
            lines_to_write.append(row)
        else:
            skip_header = False

    # Move the file cursor to the beginning
    file.seek(0)
    file.truncate()

    # Write the remaining rows without duplicate headers
    writer.writerows(lines_to_write)
