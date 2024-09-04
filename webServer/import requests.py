import requests
import json


url = "https://127.0.0.1:5001/api/recon-run/"

payload = {
    'token': '06aff1dc5192f0da53188527021255822079ce86',
    'job_name': 'CSVTest2',
    'start_date': '2024-05-31 16:04:46',
    'end_date': '2024-06-03 16:04:46', 
    'ipaddress':'216.10.243.64,172.86.96.87',
    'output_type': 'StealthWatch'
}

headers = {
    'Content-Type': "application/json",
    }

response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
csvData = response.content.decode("utf-8")
with open('CSVTest.csv', 'w') as outputFile:
    print(csvData, file=outputFile)
