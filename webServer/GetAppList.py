import requests
import json
import time
import logging

import http.client

from datetime import datetime


#http.client.HTTPConnection.debuglevel = 1
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True


session = requests.Session()

token_url = "https://vra.atrame.deloitte.com/iaas/api/login"

header = {"content-type": "application/json"}
apiToken = {
    "refreshToken": "FDbVfuDPUa13buPOqusbdHbJm4OCDfBf"
}

response = requests.post(token_url, headers=header, json=apiToken, verify=False)
x = json.loads(response.content)
bearer = x['token']
#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Got bearer Toker!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! " + bearer)
#print(bearer)
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
request_url = "https://vra.atrame.deloitte.com/catalog/api/items/05fac7d2-8d25-3cb8-8000-d167dc7ef12e/request"
header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
body = {
   "bulkRequestCount": 1,
    "deploymentName": "App List Python Test " + dt_string,
    "inputs": {
        "RDC": "Infrastructure Services - RDC - Regional Europe", 
        },
    "projectId": "e8b39d61-1f46-48a1-8f91-a6011d856ab5",
    "reason": "Testing API Python"   
}
response = requests.post(request_url, headers=header, json=body, verify=False)
x = json.loads(response.content)
deploymentData = x[0]
deploymentID = deploymentData["deploymentId"]
#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Got deployment ID !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! " + deploymentID)
success = False
deployment_url = "https://vra.atrame.deloitte.com/deployment/api/deployments/" + deploymentID + "?expand=resources"


while success == False:
    response = requests.get(deployment_url, headers=header, verify=False)
    x = json.loads(response.content)
    status = x["status"]
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Got Status ID !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! " + status)
    if status == "CREATE_SUCCESSFUL":
        success = True
    time.sleep(1)


"""
#time.sleep(10)
response = requests.get(deployment_url, headers=header, verify=False)
x = json.loads(response.content)
status = x["status"]
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Got Status ID !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! " + status)
"""


x = json.loads(response.content)
AppList = x["resources"][0]["properties"]["outputs"]["ApplicationDetailList"]["value"]
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Got App List !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

for AppInfo in AppList:
    data = AppInfo.split(",")
    appCode = data[0]
    name = data[1]
    rdc = data[2]
    desc = data[3]
    #print("AppCode = " + appCode + "\n" + "AppName = " + name + "\n" + "RDC = " + rdc + "\n" + "Description = " + desc)
    print("INSERT INTO temp_table_name_change_me VALUES('" + appCode + "','" + name + "','" + rdc + "','" + desc + "' );"   )
