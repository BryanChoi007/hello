import requests
import json
import time


token_url = "https://vra.atrame.deloitte.com/iaas/api/login"

header = {"content-type": "application/json"}
apiToken = {
    "refreshToken": "FDbVfuDPUa13buPOqusbdHbJm4OCDfBf"
}

response = requests.post(token_url, headers=header, json=apiToken, verify=False)
x = json.loads(response.content)
bearer = x['token']
#print(bearer)

request_url = "https://vra.atrame.deloitte.com/catalog/api/items/5adc4ec2-55fb-3936-b46b-a648c7082799/request"
header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
body = {
   "bulkRequestCount": 1,
    "deploymentName": "Hello World Testing Array11",
    "inputs": {
        "FirstName": "Doug", 
        "LastName": "Funnie"
        },
    "projectId": "3f57a3be-8169-4c67-95cf-6c0f54650212",
    "reason": "Testing API Python"   
}
response = requests.post(request_url, headers=header, json=body, verify=False)
x = json.loads(response.content)
deploymentData = x[0]
deploymentID = deploymentData["deploymentId"]
success = False

while success == False:
    deployment_url = "https://vra.atrame.deloitte.com/deployment/api/deployments/" + deploymentID + "?expand=resources"
    response = requests.get(deployment_url, headers=header, verify=False)
    x = json.loads(response.content)
    status = x["status"]
    if status == "CREATE_SUCCESSFUL":
        success = True
    time.sleep(1)

x = json.loads(response.content)
Names = x["resources"][0]["properties"]["outputs"]["Name"]["value"]
print(Names)