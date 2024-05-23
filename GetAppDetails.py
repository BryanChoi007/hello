import requests
import json
import time

from datetime import datetime


token_url = "https://vra.atrame.deloitte.com/iaas/api/login"

header = {"content-type": "application/json"}
apiToken = {
    "refreshToken": "FDbVfuDPUa13buPOqusbdHbJm4OCDfBf"
}

response = requests.post(token_url, headers=header, json=apiToken, verify=False)
x = json.loads(response.content)
bearer = x['token']
#print(bearer)
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
request_url = "https://vra.atrame.deloitte.com/catalog/api/items/57a6ed4d-348d-3c87-930b-493fd8c7f902/request"
header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
body = {
   "bulkRequestCount": 1,
    "deploymentName": "App Detail Python Test " + dt_string,
    "inputs": {
        "AppID": "APP1973", 
        },
    "projectId": "e8b39d61-1f46-48a1-8f91-a6011d856ab5",
    "reason": "Testing API Python"   
}
response = requests.post(request_url, headers=header, json=body, verify=False)
x = json.loads(response.content)
deploymentData = x[0]
deploymentID = deploymentData["deploymentId"]
success = False
deployment_url = "https://vra.atrame.deloitte.com/deployment/api/deployments/" + deploymentID + "?expand=resources"

while success == False:
    response = requests.get(deployment_url, headers=header, verify=False)
    x = json.loads(response.content)
    status = x["status"]
    if status == "CREATE_SUCCESSFUL":
        success = True
    time.sleep(2)

x = json.loads(response.content)
AppInfo = x["resources"][0]["properties"]["outputs"]["AppInformation"]["value"]
data = AppInfo.split(",")
appCode = data[0]
name = data[1]
rdc = data[2]
desc = data[3]
print("AppCode = " + appCode + "\n" + "AppName = " + name + "\n" + "RDC = " + rdc + "\n" + "Description = " + desc)