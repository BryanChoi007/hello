import requests
import json
import time
import datetime
import urllib.parse
import ipfix
import socket
import ipaddress
import pandas as pd

from flask import Flask, request, render_template, send_file


######################################################################## IPFIX member Variables #########################################################################
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("10.254.162.85", 2055)
domain_id = 16777217


# Define the IPFIX template
template_spec_list_4_4 = [
            "sourceIPv4Address",  # 8
            "destinationIPv4Address",  # 12
            "sourceTransportPort",  # 7
            "destinationTransportPort",  # 11
            "octetDeltaCount",  # 1
            "packetDeltaCount",  # 2
            "ingressInterface",  # 10
            "egressInterface",  # 14
            "protocolIdentifier",  # 4
            "tcpControlBits",  # 6
            #"flowSensorApplicationID",  # 29820
            #"flowSensorApplicationDetails",  # 29832
            "flowStartMilliseconds",
            #"flowEndMilliseconds",
            "ipClassOfService",
            "userName"]

template_id_4_4 = 337

ipfix.ie.use_iana_default()
ipfix.ie.for_spec("flowSensorApplicationID(8712/29820)<unsigned32>")
ipfix.ie.for_spec("flowSensorApplicationDetails(8712/29832)<string>")

template_4_4 = ipfix.template.from_ielist(template_id_4_4, ipfix.ie.spec_list(template_spec_list_4_4))

##########################################################################################################################################################################



#################################################################### Pure Signal Member Variables #########################################################################
url = "https://recon.cymru.com/api/jobs"

payload = ""
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Token 06aff1dc5192f0da53188527021255822079ce86"
    }

##############################################################################################################################################################################





app = Flask(__name__)


apiToken = {
    "refreshToken": "kPOY5kofrGKL70DTLG0rufV2KivApOTM"
}


@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/buttons.html')
def buttons():
    return render_template('buttons.html')

@app.route('/cards.html')
def cards():
    return render_template('cards.html')




#For the App Code Only. Returns Single Applicaiton Detail
@app.route('/app-info/', methods=["GET","POST"])
def app_info():
#if request.method == "POST":
    # getting input with name = fname in HTML form
    appCode = request.args.get("id")
    # getting input with name = lname in HTML form
    #last_name = request.form.get("lname")
    #return "Your name is "+first_name + last_name
    token_url = "https://vra.atrame.deloitte.com/iaas/api/login"

    header = {"content-type": "application/json"}
    #apiToken = {
    #    "refreshToken": "a1SSmflhkd9SEgvWb2idhYQbyE3R6djO"
    #}

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
            "AppID": appCode, 
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
    #appCode = data[0]
    name = data[1]
    rdc = data[2]
    desc = data[3]
    #appDataTable = "<head><style>table, th, td {border: 1px solid black;}</style></head><body>"
    #appDataTable = "<div class='container'><table><thead><tr><th>AppCode</th><th>Name</th><th>RDC</th><th>Description</th></tr></thead>"
    appDataTable = "<div class='table-wrapper'><table class='fl-table'><thead><tr><th>AppCode</th><th>Name</th><th>RDC</th><th>Description</th></tr></thead><tbody>"
    appDataTable += "<tr><td>" + appCode + "</td><td>" + name + "</td><td>" + rdc + "</td><td>" + desc + "</td></tr>"
    appDataTable += "</tbody></table></div>"

    return render_template("index3.html", result=appDataTable, title = "Application Details for " + appCode)
    #return appDataTable
    #return render_template("index.html")





 

######################################################################### Pure Signal Test ########################################################################################

#AGet Recon Results for specifci Jobs
@app.route('/recon-results/', methods=["GET","POST"])
def recon_results():
    jobName = request.args.get("title")


    response = requests.request("GET", url, data=payload, headers=headers)
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!" + response.content.decode("utf-8"))
    x = json.loads(response.content)


    #Get the ID of the specific Job that has been completed
    jobs = x["data"]

    id = -1

    for job in jobs:
        name = job["name"]
        if name == jobName:
            status = job["status"]
            if status == "Completed":
                id = job["id"]
                print(id)
                break

    if id != -1:
        response = requests.request("GET", url + "/" + str(id), data=payload, headers=headers)

        dataByte = response.content
        dataString = dataByte.decode("utf-8")
        dataArray = dataString.split("\n")
        dataArray.pop()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        convert_json_to_ipfix(dataArray)
        s.close()

        resultsTable = "<div class='table-wrapper'><table class='fl-table'><thead><tr><th>Start Time</th><th>Source IP</th><th>Source Country Code</th><th>Source Port</th><th>Destination IP</th><th>Destiantion Country Code</th><th>Destination Port</th></tr></thead><tbody>"

        #queryResults = json.loads(response.content)
        for element in dataArray:
            # Print each element
            #print(element)
        
            x = json.loads(element)
            
            query_type = x["query_type"]

            if query_type == "flows":

                start_time = x["start_time"]
                src_ip = x["src_ip_addr"]
                src_cc = x["src_cc"]
                dst_ip = x["dst_ip_addr"]
                dst_cc = x["dst_cc"]
                proto = x["proto"]
                src_port = x["src_port"]
                dst_port = x["dst_port"]
                tcp_flags = x["tcp_flags"]
                num_pkts = x["num_pkts"]
                num_octets = x["num_octets"]
                sample_algo = x["sample_algo"]
                sample_interval = x["sample_interval"]
        
                resultsTable += "<tr><td>" + start_time + "</td><td>" + src_ip + "</td><td>" + src_cc + "</td><td>" + str(src_port) + "</td><td>" + dst_ip + "</td>" + "<td>" + dst_cc + "<td>" + str(dst_port) + "</td></tr>"

        resultsTable += "</tbody></table></div>"
        return render_template("index3.html", result=resultsTable, jobID="Job ID: " + str(id), title=jobName)


def send_template():
    # Create the template and send
    message = ipfix.message.MessageBuffer()
    message.begin_export(domain_id)
    message.add_template(template_4_4)

    byte_message = message.to_bytes()
    message.begin_export(domain_id)
    message.from_bytes(byte_message)
    sent = s.sendto(message.to_bytes(), address)
    #print("Sending Template Data: " + str(sent))

    
def send_data_to_flow_collector(ipfix_data):
    # Send the IPFIX data to the flow collector
    sent = s.sendto(ipfix_data.to_bytes(), address)
    #print("Sending IPFIX Record Data " + str(sent))


def convert_json_to_ipfix(dataArray):
    print("Transmitting IPFIX REcord ................")

    # Convert the each JSOn from the array into IPFIX record
    #queryResults = json.loads(response.content)
    for element in dataArray:
        # Print each element
        #print(element)
    
        x = json.loads(element)
        #print(x)
        query_type = x["query_type"]
        
        if query_type == "flows":
            """"
            start_time = x["start_time"]
            src_ip = x["src_ip_addr"]
            src_cc = x["src_cc"]
            dst_ip = x["dst_ip_addr"]
            dst_cc = x["dst_cc"]
            proto = x["proto"]
            src_port = x["src_port"]
            dst_port = x["dst_port"]
            tcp_flags = x["tcp_flags"]
            num_pkts = x["num_pkts"]
            num_octets = x["num_octets"]
            sample_algo = x["sample_algo"]
            sample_interval = x["sample_interval"]
            """


            dateObj = datetime.datetime.strptime(x["start_time"],"%Y-%m-%d %H:%M:%S")
            milliseconds = int(dateObj.timestamp() * 1000)

            ipfix_record = {
                "sourceIPv4Address": ipaddress.ip_address(x["src_ip_addr"]),
                "destinationIPv4Address": ipaddress.ip_address(x["dst_ip_addr"]),
                "sourceTransportPort": int(x["src_port"]),
                "destinationTransportPort": int(x["dst_port"]),
                "octetDeltaCount": int(x["num_octets"]),
                "packetDeltaCount": int(x["num_pkts"]),
                "ingressInterface": 1,
                "egressInterface": 1,
                "protocolIdentifier": int(x["proto"]),
                "tcpControlBits": int(x["tcp_flags"]),
                #"flowSensorApplicationID": 10019,
                #"flowSensorApplicationDetails": record["flowSensorApplicationDetails"],
                "flowStartMilliseconds": datetime.datetime.fromtimestamp(milliseconds / 1000),
                #"flowEndMilliseconds": datetime.datetime.fromtimestamp(milliseconds / 1000),
                "ipClassOfService":0,
                "userName": "Pure Signal"
                }
            
            record_message = ipfix.message.MessageBuffer()
            record_message.begin_export(domain_id)
            record_message.add_template(template_4_4 , export=False)

            record_message.export_ensure_set(template_id_4_4)
            record_message.export_namedict(ipfix_record)

            byte_message = record_message.to_bytes()
            record_message.begin_export(domain_id)
            record_message.from_bytes(byte_message)
            #record_message.export_namedict(template_4_4,ipfix_record)
            send_template()
            send_data_to_flow_collector(record_message)



#######################################################################################################################################################################################################################################################






######################################################################### Pure Signal API Gateway Test ########################################################################################

#AGet Recon Results for specifci Jobs
@app.route('/api/recon-results/', methods=["GET","POST"])
def recon_results_api():
    jobName = request.args.get("title")

    # Make the call to Pure signal to get the jobID
    response = requests.request("GET", url, data=payload, headers=headers)
    x = json.loads(response.content)


    #Get the ID of the specific Job that has been completed
    jobs = x["data"]

    id = -1

    for job in jobs:
        name = job["name"]
        if name == jobName:
            status = job["status"]
            if status == "Completed":
                id = job["id"]
                print(id)
                break

    if id != -1:
        response = requests.request("GET", url + "/" + str(id), data=payload, headers=headers)

        dataByte = response.content
        dataString = dataByte.decode("utf-8")
        dataArray = dataString.split("\n")
        dataArray.pop()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        count = convert_json_to_ipfix(dataArray)
        s.close()

        responseMessage = {"Number of Records Processed and transmitted to Stealth Watch" : count}
        responseJSON = json.dumps(responseMessage)
        return responseJSON

def send_template():
    # Create a new IPFIX message
    message = ipfix.message.MessageBuffer()
    message.begin_export(domain_id)
    message.add_template(template_4_4)

    byte_message = message.to_bytes()
    message.begin_export(domain_id)
    message.from_bytes(byte_message)
    sent = s.sendto(message.to_bytes(), address)
    #print("Sending Template Data: " + str(sent))

    
def send_data_to_flow_collector(ipfix_data):
    # Send the IPFIX data to the flow collector
    sent = s.sendto(ipfix_data.to_bytes(), address)
    #print("Sending IPFIX Record Data " + str(sent))


def convert_json_to_ipfix(dataArray):
    print("Transmitting IPFIX Record ................")

    # Convert the each JSOn from the array into IPFIX record
    #queryResults = json.loads(response.content)
    count = 0;
    for element in dataArray:
        # Print each element
        #print(element)
    
        x = json.loads(element)
        #print(x)
        query_type = x["query_type"]
        
        if query_type == "flows":
            """"
            start_time = x["start_time"]
            src_ip = x["src_ip_addr"]
            src_cc = x["src_cc"]
            dst_ip = x["dst_ip_addr"]
            dst_cc = x["dst_cc"]
            proto = x["proto"]
            src_port = x["src_port"]
            dst_port = x["dst_port"]
            tcp_flags = x["tcp_flags"]
            num_pkts = x["num_pkts"]
            num_octets = x["num_octets"]
            sample_algo = x["sample_algo"]
            sample_interval = x["sample_interval"]
            """


            dateObj = datetime.datetime.strptime(x["start_time"],"%Y-%m-%d %H:%M:%S")
            milliseconds = int(dateObj.timestamp() * 1000)

            ipfix_record = {
                "sourceIPv4Address": ipaddress.ip_address(x["src_ip_addr"]),
                "destinationIPv4Address": ipaddress.ip_address(x["dst_ip_addr"]),
                "sourceTransportPort": int(x["src_port"]),
                "destinationTransportPort": int(x["dst_port"]),
                "octetDeltaCount": int(x["num_octets"]),
                "packetDeltaCount": int(x["num_pkts"]),
                "ingressInterface": 1,
                "egressInterface": 1,
                "protocolIdentifier": int(x["proto"]),
                "tcpControlBits": int(x["tcp_flags"]),
                #"flowSensorApplicationID": 10019,
                #"flowSensorApplicationDetails": record["flowSensorApplicationDetails"],
                "flowStartMilliseconds": datetime.datetime.fromtimestamp(milliseconds / 1000),
                #"flowEndMilliseconds": datetime.datetime.fromtimestamp(milliseconds / 1000),
                "ipClassOfService":0,
                "userName": "Pure Signal"
                }
            
            record_message = ipfix.message.MessageBuffer()
            record_message.begin_export(domain_id)
            record_message.add_template(template_4_4 , export=False)

            record_message.export_ensure_set(template_id_4_4)
            record_message.export_namedict(ipfix_record)

            byte_message = record_message.to_bytes()
            record_message.begin_export(domain_id)
            record_message.from_bytes(byte_message)
            #record_message.export_namedict(template_4_4,ipfix_record)
            send_template()
            send_data_to_flow_collector(record_message)
            count+=1
    return count

#####################################################################################################################################################

######################################################## Pure Signal API Run Test with JSON Body #############################################################
#AGet Recon Results for specifci Jobs
@app.route('/api/recon-run/', methods=["GET","POST"])
def recon_run_api():
    #jobName = request.args.get("title")


    inputs = request.get_json()

    #inputs = json.loads(data)

    token = inputs['token']
    jobName = inputs['job_name']
    startDate = inputs["start_date"]
    endDate = inputs["end_date"]
    ipAddress = inputs["ipaddress"]
    outputType = inputs["output_type"]


    print("Token: " + token)
    print("Job Name: " + jobName)
    print("Start Date: " + startDate)  
    print("End Date: " + endDate)
    print("IPAddress: " + ipAddress)

    payload = {
        'job_name': jobName,
        'job_description': 'API Gateway Run',
        'start_date': startDate,
        'end_date': endDate,
        'priority': 25,
        'queries' : [
            {
                'query_type':'flows',
                'any_ip_addr':ipAddress,
                #'any_port':10
            }
        ]
    }

    headers = {
    'Content-Type': "application/json",
    'Authorization': "Token " + token
    }

    response = requests.request("POST", url , data=json.dumps(payload), headers=headers)
    #returnStr = "{\"Token\": \"" + token + "\",\"JobName\": \"" + jobName + "\"}"

    jsonResponse = json.loads(response.content)

    jobID = jsonResponse["job"]["id"]

    print("!!!!!! JOB ID !!!!!!! " + str(jobID))

# we will poll the jobID until it is completed. Once completed we can run the get results query.


    status = ""
    payload = ""
    while status != "Completed":
        print("checking to see if jobID: " + str(jobID) + " has completed!!!!!!!!!!!!!!!!!!!!!!")
        response = requests.request("GET", url, data=payload, headers=headers)
        x = json.loads(response.content)


        #Get the ID of the job to ompare with our jobID
        jobs = x["data"]

        for job in jobs:
            id = job["id"]
            if jobID == id:
                status = job["status"]
                if status == "Completed":
                    jobName = job["name"]
                    print("Job: " + jobName + " has completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    break
        if status != "Completed":
            time.sleep(60)



# Get the results for the jobID that just completed.

    response = requests.request("GET", url + "/" + str(jobID), data=payload, headers=headers)
    dataByte = response.content
    dataString = dataByte.decode("utf-8")


    if outputType == "StealthWatch":
        print("Output Type is " + outputType + " calling recon_run_api() function!!!!!!!!!!!!!!!!!!")
        headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        }

        apiGatewayURL = "https://127.0.0.1:5001/api/recon-results?title=" + jobName
        response = requests.request("GET", apiGatewayURL, data=payload, headers=headers)
        dataByte = response.content
        responseMessage =  dataByte.decode("utf-8")
        return responseMessage
    
    elif outputType == "csv":
        dataArray = dataString.split("\n")
        dataArray.pop()

        csvOutput = "Start Time,Source IP,Source Country Code,Source Port,Destination IP,Destiantion Country Code,Destination Port\n"

        #queryResults = json.loads(response.content)
        for element in dataArray:
            # Print each element
            #print(element)
        
            x = json.loads(element)
            
            query_type = x["query_type"]

            if query_type == "flows":

                start_time = x["start_time"]
                src_ip = x["src_ip_addr"]
                src_cc = x["src_cc"]
                dst_ip = x["dst_ip_addr"]
                dst_cc = x["dst_cc"]
                proto = x["proto"]
                src_port = x["src_port"]
                dst_port = x["dst_port"]
                tcp_flags = x["tcp_flags"]
                num_pkts = x["num_pkts"]
                num_octets = x["num_octets"]
                sample_algo = x["sample_algo"]
                sample_interval = x["sample_interval"]
        
                csvOutput += start_time + "," + src_ip + "," + src_cc + "," + str(src_port) + "," + dst_ip + "," + dst_cc + "," + str(dst_port) + "\n"

        print("Output Type is " + outputType + " returning the CSV Format!!!!!!!!!!!!!!!!!!")
        return csvOutput

    else:
        print("Output Type is " + outputType + " returning the JSON!!!!!!!!!!!!!!!!!!")
        return dataString



    

    """
    headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Token " + token
    }

    # Make the call to Pure signal to get the jobID
    response = requests.request("GET", url, data=payload, headers=headers)
    x = json.loads(response.content)


    return count
    """


#####################################################################################################################################################


######################################################### Download Testing ####################################################################

@app.route('/api/downloadTest', methods=["GET","POST"])
def download_test():

    # Create a dataframe and save as a CSV file
    data = {'Name': ['John', 'Anna', 'Peter'], 
            'Age': [28, 23, 39]}
    df = pd.DataFrame(data)
    df.to_csv('users.csv', index=False)

    return send_file('users.csv', as_attachment=True)

    #return appDataTable
#return render_template("index.html")



#######################################################################################################################################################################################################################################################














# Get List of Tenants
@app.route('/tenant-list/', methods=["GET","POST"])
def tenant_list():
    #country = request.args.get("id")
    #print("!!!!!!!!!!!!!!!!!!!! Country is " + urllib.parse.unquote(country))
    #if request.method == "POST":

    # getting input with name = fname in HTML form
    #rdc = request.form.get("RDC")
    # getting input with name = lname in HTML form
    #last_name = request.form.get("lname")
    #return "Your name is "+first_name + last_name
    token_url = "https://vra.atrame.deloitte.com/iaas/api/login"

    header = {"content-type": "application/json"}
    #apiToken = {
    #    "refreshToken": "MaiZziVKcfcgEXv6MDobi51b3kGGuExS"
    #}

    response = requests.post(token_url, headers=header, json=apiToken, verify=False)
    x = json.loads(response.content)
    bearer = x['token']
    #print(bearer)
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    request_url = "https://vra.atrame.deloitte.com/catalog/api/items/38e5b74f-451d-3a90-971c-02ede7b4b958/request"
    header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
    body = {
        "bulkRequestCount": 1,
        "deploymentName": "Tenant List Python Test " + dt_string,
        "inputs": {
            "ActionType": "List" 
            },
        "projectId": "128e9e03-f32d-4789-968e-f9e959adf44c",
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
    #appDataTable = "<h1>Application Information</h1><h2>Total Count: {{ count | safe }}</h2>"

    tenantDataTable = "<div class='table-wrapper'><table class='fl-table'><thead><tr><th>Tenant</th><th>Description</th></tr></thead><tbody>"
    #appDataTable = ""
    x = json.loads(response.content)
    TenantList = x["resources"][0]["properties"]["outputs"]["TenantList"]["value"]
    tenantCount = len(TenantList)
    for Tenant in TenantList:

        data = Tenant.split(",")
        name = data[0]
        desc = data[1]


        tenantDataTable += "<tr><td>" + name + "</td><td>" + desc + "</td></tr>"
    #appDataTable = "<head><style>table, th, td {border: 1px solid black;}</style></head><body>"
    
    
    
    tenantDataTable += "</tbody></table></div>"
    
    return render_template("index3.html", result=tenantDataTable, count="Total Count: " + str(tenantCount), title="Tenant Information")
    #return appDataTable
#return render_template("index.html")



# Get List of F5 Pools
@app.route('/pool-list/', methods=["GET","POST"])
def pool_list():
    #country = request.args.get("id")
    #print("!!!!!!!!!!!!!!!!!!!! Country is " + urllib.parse.unquote(country))
    #if request.method == "POST":

    # getting input with name = fname in HTML form
    #rdc = request.form.get("RDC")
    # getting input with name = lname in HTML form
    #last_name = request.form.get("lname")
    #return "Your name is "+first_name + last_name
    token_url = "https://vra.atrame.deloitte.com/iaas/api/login"

    header = {"content-type": "application/json"}
    #apiToken = {
    #    "refreshToken": "MaiZziVKcfcgEXv6MDobi51b3kGGuExS"
    #}

    response = requests.post(token_url, headers=header, json=apiToken, verify=False)
    x = json.loads(response.content)
    bearer = x['token']
    #print(bearer)
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    request_url = "https://vra.atrame.deloitte.com/catalog/api/items/f1dfe174-3662-35ef-92b8-7ec392567bd0/request"
    header = {"content-type": "application/json","Authorization": "Bearer " + bearer}
    body = {
        "bulkRequestCount": 1,
        "deploymentName": "Tenant List Python Test " + dt_string,
        "inputs": {
            },
        "projectId": "3f57a3be-8169-4c67-95cf-6c0f54650212",
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
    #appDataTable = "<h1>Application Information</h1><h2>Total Count: {{ count | safe }}</h2>"

    poolDataTable = "<div class='table-wrapper'><table class='fl-table'><thead><tr><th>Name</th><th>Partition</th><th>Monitor</th><th>Members</th></tr></thead><tbody>"
    #appDataTable = ""
    x = json.loads(response.content)
    PoolList = x["resources"][0]["properties"]["outputs"]["PoolList"]["value"]
    poolCount = len(PoolList)
    for Pool in PoolList:

        data = Pool.split(",")
        name = data[0]
        partition = data[1]
        monitor = data[2]

        memberList = str(data[3]).replace("|","<br>")


        poolDataTable += "<tr><td>" + name + "</td><td>" + partition + "</td><td>" + monitor + "</td><td>" + memberList + "</td></tr>"
    #appDataTable = "<head><style>table, th, td {border: 1px solid black;}</style></head><body>"
    
    
    
    poolDataTable += "</tbody></table></div>"
    
    return render_template("index3.html", result=poolDataTable, count="Total Count: " + str(poolCount), title="F5 Pool Information")
    #return appDataTable
#return render_template("index.html")



if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5001,debug=True, ssl_context="adhoc")
    #app.run(debug=True)