import json
from scapy.all import *



# Define NetFlow v9 Header
class NetFlowHeader(Packet):
    name = "NetFlowHeader"
    fields_desc = [ ShortField("version", 9),
                    ShortField("count", 1),
                    IntField("sys_uptime", 0),
                    IntField("unix_secs", 0),
                    IntField("sequence", 0),
                    IntField("source_id", 99)]

# Define NetFlow v9 Template
class NetFlowTemplate(Packet):
    name = "NetFlowTemplate"
    fields_desc = [ ShortField("template_id", 337),
                    ShortField("field_count", 7),
                    ShortField("field_type_1", 8),  # Source IP address
                    ShortField("field_length_1", 12),
                    ShortField("field_type_2", 12),  # Destination IP address
                    ShortField("field_length_2", 12),
                    ShortField("field_type_3", 7),  # Source port number
                    ShortField("field_length_3", 12),
                    ShortField("field_type_4", 11),  # Destination port number
                    ShortField("field_length_4", 12),
                    ShortField("field_type_5", 4),  # Layer 3 protocol type
                    ShortField("field_length_5", 10),
                    ShortField("field_type_6", 5),  # ToS
                    ShortField("field_length_6", 3),
                    ShortField("field_type_7", 10),  # Input logical interface
                    ShortField("field_length_7", 3)]

# Define NetFlow v9 Data
class NetFlowData(Packet):
    name = "NetFlowData"
    fields_desc = [ IPField("src_ip", "0.0.0.0"),
                    IPField("dst_ip", "0.0.0.0"),
                    ShortField("src_port", 0),
                    ShortField("dst_port", 0),
                    ByteField("protocol", 0),
                    ByteField("tos", 0),
                    ShortField("input_iface", 0)]

# Parse Pure Signal JSON data
pure_signal_data = '{"start_time": "2024-04-11 12:28:05", "src_ip_addr": "102.216.125.4", "src_cc": "ZA", "dst_ip_addr": "216.10.243.64", "dst_cc": "IN", "proto": 6, "src_port": 52934, "dst_port": 80, "tcp_flags": 20, "num_pkts": 1, "num_octets": 52, "sample_algo": 0, "sample_interval": 0, "query_type": "flows"}'
data_list = json.loads(pure_signal_data)

# Create and send NetFlow packet for each data input
#for data in data_list:
#print(data_list["src_ip_addr"])

packet = IP(dst="10.254.162.85")/UDP(dport=2055)/NetFlowHeader()/NetFlowTemplate()/NetFlowData(src_ip=data_list["src_ip_addr"], dst_ip=data_list["dst_ip_addr"], src_port=data_list["src_port"], dst_port=data_list["dst_port"], protocol=data_list["proto"], tos=0, input_iface=0)
#packet = IP(src="10.29.171.143",dst="10.254.162.85")/UDP(dport=2055)/NetFlowHeader()/NetFlowTemplate()/NetFlowData(src_ip=data_list["src_ip_addr"], dst_ip=data_list["dst_ip_addr"], src_port=data_list["src_port"], dst_port=data_list["dst_port"], protocol=data_list["proto"], tos=0, input_iface=0)

print(scapy.VERSION)
#print(conf.route)
#packet.show()

send(packet)
#scapy.all.send(packet, iface = "Intel(R) Wi-Fi 6E AX211 160MHz")

#Get a list of network interfaces
#interfaces = get_if_list()
#print(conf.route.route("10.254.162.85"))
#conf.route.resync()
#print(conf.ifaces)
#conf.route.add(("0.0.0.0", "0.0.0.0", "192.168.1.1"))

# Print the list of interfaces
#for interface in interfaces:
#    print(interface)
#conf.route.resync()
#print(conf.ifaces)
