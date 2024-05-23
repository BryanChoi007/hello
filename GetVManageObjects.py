import requests
import json
import time
from datetime import datetime
import sys


#Get the bearer token with the API token for current credentials
token_url = "https://vra.atrame.deloitte.com/iaas/api/login"
header = {"content-type": "application/json"}
apiToken = {
    "refreshToken": "a1SSmflhkd9SEgvWb2idhYQbyE3R6djO"
}

response = requests.post(token_url, headers=header, json=apiToken, verify=False)
x = json.loads(response.content)
bearer = x['token']



#Request the VManage Tenant List Workflow and get the deployment ID.
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

request_url = "https://vra.atrame.deloitte.com/catalog/api/items/26a2653e-66d9-3509-8f71-ffeaf8c7cfaf/request"
header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
body = {
    "bulkRequestCount": 1,
    "deploymentName": "Get VManage Tenant List" + dt_string,
    "inputs": {
        },
    "projectId": "90b326ff-10d8-4494-a99e-7548b93f3d60",
    "reason": "SD-WAN vManage Object CSV Writer"   
}
response = requests.post(request_url, headers=header, json=body, verify=False)
x = json.loads(response.content)
deploymentData = x[0]
deploymentID = deploymentData["deploymentId"]
success = False

#Get deploymentID and check to see status. If sucessful then get List of Tenant from output
deployment_url = "https://vra.atrame.deloitte.com/deployment/api/deployments/" + deploymentID + "?expand=resources"


while success == False:
    response = requests.get(deployment_url, headers=header, verify=False)
    x = json.loads(response.content)
    status = x["status"]
    if status == "CREATE_SUCCESSFUL":
        success = True
    time.sleep(2)

x = json.loads(response.content)
tenantList = x["resources"][0]["properties"]["outputs"]["TenantList"]["value"]

#file to write
with open('vManage.csv', 'w') as outputFile:

    for tenantInfo in tenantList:
        print("Tenant Info: " + tenantInfo)
        data = tenantInfo.split("|")
        tenant = data[0]
        print("Tenant: " + tenant)
        id = data[1]

        # Get the device Template per tenant
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        request_url = "https://vra.atrame.deloitte.com/catalog/api/items/37be1ba3-9787-3d3a-a25f-51413e136915/request"
        header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
        body = {
            "bulkRequestCount": 1,
            "deploymentName": "Get VManage Device Template per Tenant " + dt_string,
            "inputs": {
                "Tenant": tenantInfo 
                },
            "projectId": "90b326ff-10d8-4494-a99e-7548b93f3d60",
            "reason": "SD-WAN vManage Object CSV Writer"   
        }
        response = requests.post(request_url, headers=header, json=body, verify=False)
        x = json.loads(response.content)
        deploymentData = x[0]
        deploymentID = deploymentData["deploymentId"]
        success = False

        #Get deploymentID and check to see status. If sucessful then get List of Device Templates from output
        deployment_url = "https://vra.atrame.deloitte.com/deployment/api/deployments/" + deploymentID + "?expand=resources"


        while success == False:
            response = requests.get(deployment_url, headers=header, verify=False)
            x = json.loads(response.content)
            status = x["status"]
            if status == "CREATE_SUCCESSFUL":
                success = True
            time.sleep(2)

        x = json.loads(response.content)
        deviceTemplateList = x["resources"][0]["properties"]["outputs"]["DeviceTemplates"]["value"]
        for deviceTemplate in deviceTemplateList:
            data = deviceTemplate.split("|")
            deviceName = data[0]
            deviceID = data[1]

            #Get the feature Templates per Device Template
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            request_url = "https://vra.atrame.deloitte.com/catalog/api/items/99ef4ec4-d5f9-3d8a-9adf-0d678c527dec/request"
            header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
            body = {
                "bulkRequestCount": 1,
                "deploymentName": "Get VManage Feature Template per Device " + dt_string,
                "inputs": {
                    "Tenant": tenantInfo,
                    "TemplateID": deviceID 
                    },
                "projectId": "90b326ff-10d8-4494-a99e-7548b93f3d60",
                "reason": "SD-WAN vManage Object CSV Writer"   
            }
            response = requests.post(request_url, headers=header, json=body, verify=False)
            x = json.loads(response.content)
            deploymentData = x[0]
            deploymentID = deploymentData["deploymentId"]
            success = False

            #Get deploymentID and check to see status. If sucessful then get List of Feature Templates from output
            deployment_url = "https://vra.atrame.deloitte.com/deployment/api/deployments/" + deploymentID + "?expand=resources"


            while success == False:
                response = requests.get(deployment_url, headers=header, verify=False)
                x = json.loads(response.content)
                status = x["status"]
                if status == "CREATE_SUCCESSFUL":
                    success = True
                time.sleep(2)

            x = json.loads(response.content)
            featureTemplateList = x["resources"][0]["properties"]["outputs"]["FeatureTemplateList"]["value"]
            for featureTemplate in featureTemplateList:
                data = featureTemplate.split("|")
                featureName = data[0]
                featureID = data[1]

                print(tenant + "," + deviceName + "," + featureName, file=outputFile)

        





"""""
for i in range(8,10):
    for j in alc:
        for k in alc:
            api_url = "https://licenseplatedata.com/consumer-api/SAMIR-LPDKV2F1Y/MD/" + str(i) + j + k + "6100"
            print(api_url)
            response = requests.get(api_url)
            print(response.content)
            if not response.content.startswith(b'<!DOCTYPE html>') and not response.content.startswith(b'<html>\n<head><title>500 Internal Server Error'):
                x = json.loads(response.content)
                if x["code"] != 404:
                    year = x["licensePlateLookup"]["year"]
                    make = x["licensePlateLookup"]["make"].upper()
                    model = x["licensePlateLookup"]["model"].upper()
                    print(year + " " + make + " " + model)
                    if make == 'TOYOTA' and model == 'TACOMA':
                        with open('vehicle.txt', 'a') as f:
                            print(str(i) + j + k + "6100" + " " + x["licensePlateLookup"]["name"] + " " + x["licensePlateLookup"]["vin"] + "\n", file=f)
                            #break_out_flag = True
                            #break
                time.sleep(2.6)
            #if break_out_flag:
                #break

        #if break_out_flag:
            #break       

#api_url = "https://licenseplatedata.com/consumer-api/BRYAN-LPDNL6CXN/TX/794S3S"
#response = requests.get(api_url)
#print(response.content)
#x = json.loads(response.content)
#print(x["licensePlateLookup"]["year"])
"""