import socket
import ipfix
import ipaddress
from ipaddress import IPv4Address,IPv6Address

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("10.254.162.85", 2055)
domain_id = 2218


# Create the template
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
            "flowSensorApplicationID",  # 29820
            "flowSensorApplicationDetails",  # 29832
            "flowStartMilliseconds",
            "flowEndMilliseconds",
            "ipClassOfService",
            "userName"]

template_id_4_4 = 337

ipfix.ie.use_iana_default()
ipfix.ie.for_spec("flowSensorApplicationID(8712/29820)<unsigned32>")
ipfix.ie.for_spec("flowSensorApplicationDetails(8712/29832)<string>")

template_4_4 = ipfix.template.from_ielist(template_id_4_4, ipfix.ie.spec_list(template_spec_list_4_4))

msg = ipfix.message.MessageBuffer
#msg.begin_export(domain_id)
msg.add_template(template_4_4)
byte_message = msg.to_bytes()
#msg.begin_export(domain_id)
msg.from_bytes(byte_message)
sock.sendto(msg.to_bytes(), address)


# create the record message and send
record = {"sourceIPv4Address": "192.0.2.1", "destinationIPv4Address": "192.0.2.2"}

record_message = ipfix.message.MessageBuffer()
#record_message.begin_export(domain_id)
record_message.add_template(template_spec_list_4_4, export=False)

record_message.export_ensure_set(template_id_4_4 )
record_message.export_namedict(record)

byte_message = record_message.to_bytes()
record_message.begin_export(domain_id)
record_message.from_bytes(byte_message)

#flow_collector_ip = "10.254.162.85"  # Replace with your Flow Collector's IP
#flow_collector_port = 2055  # Replace with your Flow Collector's port
sock.sendto(record_message.finish(), address)