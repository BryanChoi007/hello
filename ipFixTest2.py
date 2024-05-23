import ipfix
import socket
import json
import ipaddress
#from ipaddress import IPv4Address,IPv6Address
import datetime


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


def convert_json_to_ipfix(json_data):
    """"
    ipfix.ie.use_iana_default()
    ipfix.ie.for_spec("flowSensorApplicationID(8712/29820)<unsigned32>")
    ipfix.ie.for_spec("flowSensorApplicationDetails(8712/29832)<string>")

    template_4_4 = ipfix.template.from_ielist(template_id_4_4, ipfix.ie.spec_list(template_spec_list_4_4))

    # Create a new IPFIX message
    message = ipfix.message.MessageBuffer()
    message.begin_export(domain_id)
    message.add_template(template_4_4)

    byte_message = message.to_bytes()
    message.begin_export(domain_id)
    message.from_bytes(byte_message)
    sent = s.sendto(message.to_bytes(), address)
    print("Sending Template Data: " + str(sent))
    """


    
    # Export the template to the message
    #message.export_template(template_4_4)

    # Convert the JSON data to IPFIX

    ipfix_record = {}
    for record in json_data:

        print(record["flowStartMilliseconds"])
        dateObj = datetime.datetime.strptime(record["flowStartMilliseconds"],"%Y-%m-%d %H:%M:%S")
        milliseconds = int(dateObj.timestamp() * 1000)

        ipfix_record = {
            "sourceIPv4Address": ipaddress.ip_address(record["sourceIPv4Address"]),
            "destinationIPv4Address": ipaddress.ip_address(record["destinationIPv4Address"]),
            "sourceTransportPort": int(record["sourceTransportPort"]),
            "destinationTransportPort": int(record["destinationTransportPort"]),
            "octetDeltaCount": int(record["octetDeltaCount"]),
            "packetDeltaCount": int(record["packetDeltaCount"]),
            "ingressInterface":1,
            "egressInterface": 1,
            "protocolIdentifier": int(record["protocolIdentifier"]),
            "tcpControlBits": int(record["tcpControlBits"]),
            #"flowSensorApplicationID": 10019,
            #"flowSensorApplicationDetails": record["flowSensorApplicationDetails"],
            "flowStartMilliseconds": datetime.datetime.fromtimestamp(milliseconds / 1000),
            #"flowEndMilliseconds": datetime.datetime.fromtimestamp(milliseconds / 1000),
            "ipClassOfService": int(record["ipClassOfService"]),
            "userName": record["userName"]
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

# Load your JSON data
json_data = [
    {
        "sourceIPv4Address": "192.168.1.110",
        "destinationIPv4Address": "192.168.1.111",
        "sourceTransportPort": 443,
        "destinationTransportPort": 80,
        "octetDeltaCount": 200,
        "packetDeltaCount": 10,
        "ingressInterface": 1,
        "egressInterface": 2,
        "protocolIdentifier": 6,
        "tcpControlBits": 24,
        "flowSensorApplicationID": "Test",
        "flowSensorApplicationDetails": "",
        "flowStartMilliseconds": "2024-04-11 12:28:05",
        "flowEndMilliseconds": "2024-04-11 12:28:05",
        "ipClassOfService": 20,
        "userName": "Pure Signal"
    },
    {
        "sourceIPv4Address": "192.168.1.112",
        "destinationIPv4Address": "192.168.1.113",
        "sourceTransportPort": 443,
        "destinationTransportPort": 80,
        "octetDeltaCount": 200,
        "packetDeltaCount": 10,
        "ingressInterface": 1,
        "egressInterface": 2,
        "protocolIdentifier": 6,
        "tcpControlBits": 24,
        "flowSensorApplicationID": "Test",
        "flowSensorApplicationDetails": "",
        "flowStartMilliseconds": "2024-04-11 12:28:05",
        "flowEndMilliseconds": "2024-04-11 12:28:05",
        "ipClassOfService": 20,
        "userName": "Pure Signal"
    }
    # Add more records as needed...
]

# Convert the JSON data to IPFIX
#message = "Hello, Server!"
#ipfix_data = message.encode()  
convert_json_to_ipfix(json_data)
s.close()
# Send the IPFIX data to the flow collector
#send_template()
#send_data_to_flow_collector(ipfix_data.to_bytes())