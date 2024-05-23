import requests

# SharePoint credentials
username = 'alamin.bantan@kaust.edu.sa'
password = 'Ab1112990562067426!'

# URL of the SharePoint folder
sharepoint_url = 'https://kaust.sharepoint.com/:f:/r/sites/M365_CDA_CEA_Team/Shared%20Documents/MiniGH_experiments/climatic%20data?csf=1&web=1&e=XmtkF7'

# Path to your CSV file on Raspberry Pi
csv_file_path = '/home/cdacea/south_GH/south_climate.csv'

# Read the content of the CSV file
with open(csv_file_path, 'rb') as file:
    file_content = file.read()

# SharePoint upload URL
upload_url = sharepoint_url + '/' + 'south_climate.csv'

# SharePoint API requires the correct headers
headers = {
    'Accept': 'application/json;odata=verbose',
    'Content-Type': 'application/json;odata=verbose',
}

# Authenticate to SharePoint
response = requests.post(
    'https://kaust.sharepoint.com/_forms/default.aspx?wa=wsignin1.0',
    auth=(username, password),
)

# Upload the file to SharePoint
response = requests.put(
    upload_url,
    data=file_content,
    headers=headers,
    auth=(username, password)
)

if response.status_code == 200:
    print('File uploaded successfully to SharePoint.')
else:
    print('Failed to upload file to SharePoint. Status code:', response.status_code)
