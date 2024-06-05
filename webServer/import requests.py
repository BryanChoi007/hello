import requests
import json


url = "http://127.0.0.1:5000/api/recon-run"

payload = {
    "token": "06aff1dc5192f0da53188527021255822079ce86",
    "job_name": "CSVTest",
    "start_date": "2024-05-31 16:04:46",
    "end_date": "2024-06-03 16:04:46", 
    "ipaddress":"216.10.243.64,172.86.96.87",
    "output_type": "csv"
}

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    }


response = requests.request("GET", url, data=payload, headers=headers)

print(response.content.decode("utf-8"))
csvData = response.content.decode("utf-8")

#file to write
with open('CSVTest.csv', 'w') as outputFile:

    #for line in lines:
    #print("Line Info: " + line)
    print(csvData, file=outputFile)