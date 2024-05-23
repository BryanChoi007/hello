import requests
import json
import ipfix
import socket
import ipaddress
import datetime




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
    'Authorization': "Token 6e0d63aa0c472fa95b3a5d4b3edcf0e9ffeb1725"
    }

jobName = "BryanTest2"
##############################################################################################################################################################################


############################################################################################## Functions ######################################################################################################

def send_template():
    # Create a new IPFIX message
    message = ipfix.message.MessageBuffer()
    message.begin_export(domain_id)
    message.add_template(template_4_4)

    byte_message = message.to_bytes()
    message.begin_export(domain_id)
    message.from_bytes(byte_message)
    sent = s.sendto(message.to_bytes(), address)
    print("Sending Template Data: " + str(sent))


def convert_json_to_ipfix(dataArray):

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

    # Return the IPFIX message
    #return record_message

def send_data_to_flow_collector(ipfix_data):
    # Create a socket object
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send the IPFIX data to the flow collector

    sent = s.sendto(ipfix_data.to_bytes(), address)
    print("Sending IPFIX Record Data " + str(sent))
    #s.sendto(ipfix_data, (host, port))

    # Close the socket
    #s.close()


###################################################################################################################################################################################################################



########################################################################################################### Main #####################################################################################################

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

    #print(response.content)

    dataByte = response.content
    dataString = dataByte.decode("utf-8")
    dataArray = dataString.split("\n")
    dataArray.pop()
    
    convert_json_to_ipfix(dataArray)
    s.close()



