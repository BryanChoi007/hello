import datetime
import time
import ipaddress
from ipaddress import IPv4Address,IPv6Address
import socket
import os
import ipfix
import traceback
import sys
import json

class IPFix():

    REQUIRED_FIELDS = [
        "clientIPAddress",
        "serverIPAddress",
        "clientOctetDeltaCount",
        "serverOctetDeltaCount",
        "flowEndMilliseconds",
        "durationMilliseconds",
        "method",
        "url",
        "responseCode",
    ]

    HTTP_CODES = {
        "0": "Undefined code",
        "100": "Continue",
        "101": "Switching Protocols",
        "102": "Processing (WebDAV; RFC 2518)",
        "200": "OK", # The
        "201": "Created", # The request has been fulfilled, and a new resource is created
        "202": "Accepted", # The request has been accepted for processing, but the processing has not been completed
        "203": "Non-Authoritative Information", # The request has been successfully processed, but is returning information that may be from another source
        "204": "No Content", # The request has been successfully processed, but is not returning any content
        "205": "Reset Content", # The request has been successfully processed, but is not returning any content, and requires that the requester reset the document view
        "206": "Partial Content", # The server is delivering only part of the resource due to a range header sent by the client
        "300": "Multiple Choices", # A link list.The user can select a link and go to that location.Maximum five addresses
        "301": "Moved Permanently", # The requested page has moved to a new URL
        "302": "Found", # The requested page has moved temporarily to a new URL
        "303": "See Other", # The requested page can be found under a different URL
        "304": "Not Modified", # Indicates the requested page has not been modified since last requested
        "306": "Switch Proxy", # No longer used
        "307": "Temporary Redirect", # The requested page has moved temporarily to a new URL
        "308": "Resume Incomplete", # Used in the resumable requests proposal to resume aborted PUT or POST requests
        "400": "Bad Request", # The request cannot be fulfilled due to bad syntax
        "401": "Unauthorized", # The request was a legal request, but the server is refusing to respond to it.For use when authentication is possible but has failed or not yet been provided
        "402": "Payment Required", # Reserved for future use
        "403": "Forbidden", # The request was a legal request, but the server is refusing to respond to it
        "404": "Not Found", # The requested page could not be found but may be available again in the future
        "405": "Method Not Allowed", # A request was made of a page using a request method not supported by that page
        "406": "Not Acceptable", # The server can only generate a response that is not accepted by the client
        "407": "Proxy Authentication Required", # The client must first authenticate itself with the proxy
        "408": "Request Timeout", # The server timed out waiting for the request
        "409": "Conflict", # The request could not be completed because of a conflict in the request
        "410": "Gone", # The requested page is no longer available
        "411": "Length Required", # The "Content-Length" is not defined.The server will not accept the request without it
        "412": "Precondition Failed", # The precondition given in the request evaluated to false by the server
        "413": "Request Entity Too Large", # The server will not accept the request, because the request entity is too large
        "414": "Request-URI Too Long", # The server will not accept the request, because the URL is too long.Occurs when you convert a POST request to a GET request with a long query information
        "415": "Unsupported Media Type", # The server will not accept the request, because the media type is not supported
        "416": "Requested Range Not Satisfiable", # The client has asked for a portion of the file, but the server cannot supply that portion
        "417": "Expectation Failed", # The server cannot meet the requirements of the Expect request-header field
        "500": "Internal Server Error", # A generic error message, given when no more specific message is suitable
        "501": "Not Implemented", # The server either does not recognize the request method, or it lacks the ability to fulfill the request
        "502": "Bad Gateway", # The server was acting as a gateway or proxy and received an invalid response from the upstream server
        "503": "Service Unavailable", # The server is currently unavailable (overloaded or down)
        "504": "Gateway Timeout", # The server was acting as a gateway or proxy and did not receive a timely response from the upstream server
        "505": "HTTP Version Not Supported", # The server does not support the HTTP protocol version used in the request
        "511": "Network Authentication Required"
    }
    def __init__(self, dest_ip, dest_port, domain_id=2218, parent=None):
        if 'DEBUG' in os.environ:
            self.DEBUG = True
        else:
            self.DEBUG = False
        self.parent = parent
        self.dest_ip = dest_ip
        self.dest_port = dest_port
        self.domain_id = domain_id
        self.template_spec_list_4_4 = [
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
        self.template_spec_list_4_6 = [
            "sourceIPv4Address",  # 8
            "destinationIPv6Address", #28
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
        self.template_spec_list_6_4 = [
            "destinationIPv4Address",  # 12
            "sourceIPv6Address", #27
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
        self.template_spec_list_6_6 = [
            "sourceIPv6Address", #27
            "destinationIPv6Address", #28
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
        self.template_id_4_4 = 337
        self.template_id_4_6 = 338
        self.template_id_6_4 = 339
        self.template_id_6_6 = 340
        self.template_4_4, self.template_4_6, self.template_6_4, self.template_6_6 = self.create_templates()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (self.dest_ip, self.dest_port)


    def validate_data_fields(self, data):
        validation_errors = []
        for name in self.REQUIRED_FIELDS:
            if name not in data.keys():
                validation_errors.append(f'"{name}"')
        return validation_errors


    def create_templates(self):
        ipfix.ie.use_iana_default()

        # Creating the custom IE specs for Fs application id/details
        ipfix.ie.for_spec("flowSensorApplicationID(8712/29820)<unsigned32>")
        ipfix.ie.for_spec("flowSensorApplicationDetails(8712/29832)<string>")

        # Generate the template for the Flow Records
        template_4_4 = ipfix.template.from_ielist(self.template_id_4_4, ipfix.ie.spec_list(self.template_spec_list_4_4))
        template_4_6 = ipfix.template.from_ielist(self.template_id_4_6, ipfix.ie.spec_list(self.template_spec_list_4_6))
        template_6_4 = ipfix.template.from_ielist(self.template_id_6_4, ipfix.ie.spec_list(self.template_spec_list_6_4))
        template_6_6 = ipfix.template.from_ielist(self.template_id_6_6, ipfix.ie.spec_list(self.template_spec_list_6_6))

        return template_4_4, template_4_6, template_6_4, template_6_6


    def formulate_messages(self, data):

        # Add the forward and reverse records based on the event
        forward_record, reverse_record, forward_template, forward_template_id, reverse_template, reverse_template_id = self.create_record(data)
        if not forward_record or not reverse_record:
            return None

        forward_message = ipfix.message.MessageBuffer()
        forward_message.begin_export(self.domain_id)
        forward_message.add_template(forward_template, export=False)

        forward_message.export_ensure_set(forward_template_id)
        forward_message.export_namedict(forward_record)

        forward_message.export_ensure_set(reverse_template_id)
        forward_message.export_namedict(reverse_record)

        byte_message = forward_message.to_bytes()
        forward_message.begin_export(self.domain_id)
        forward_message.from_bytes(byte_message)

        # reverse_message = ipfix.message.MessageBuffer()
        # reverse_message.begin_export(self.domain_id)
        # reverse_message.add_template(reverse_template, export=False)
        # reverse_message.export_ensure_set(reverse_template_id)
        # reverse_message.export_namedict(reverse_record)
        #
        # byte_message = reverse_message.to_bytes()
        # reverse_message.begin_export(self.domain_id)
        # reverse_message.from_bytes(byte_message)

        #return forward_message, reverse_message

        return forward_message

    def formulate_templates(self):

        # Add the forward and reverse records based on the event
        template = self.template_4_4

        message1 = ipfix.message.MessageBuffer()
        message1.begin_export(self.domain_id)
        message1.add_template(template)

        # Format message for transmitting
        byte_message = message1.to_bytes()
        message1.begin_export(self.domain_id)
        message1.from_bytes(byte_message)

        template = self.template_4_6

        message2 = ipfix.message.MessageBuffer()
        message2.begin_export(self.domain_id)
        message2.add_template(template)

        # Format message for transmitting
        byte_message = message2.to_bytes()
        message2.begin_export(self.domain_id)
        message2.from_bytes(byte_message)

        template = self.template_6_4

        message3 = ipfix.message.MessageBuffer()
        message3.begin_export(self.domain_id)
        message3.add_template(template)

        # Format message for transmitting
        byte_message = message3.to_bytes()
        message3.begin_export(self.domain_id)
        message3.from_bytes(byte_message)

        template = self.template_6_6

        message4 = ipfix.message.MessageBuffer()
        message4.begin_export(self.domain_id)
        message4.add_template(template)

        # Format message for transmitting
        byte_message = message4.to_bytes()
        message4.begin_export(self.domain_id)
        message4.from_bytes(byte_message)

        return message1, message2, message3, message4

    def send_templates(self):
        template1, template2, template3, template4 = self.formulate_templates()
        try:
            self.sock.sendto(template1.to_bytes(), self.address)
            if self.DEBUG:
                print(f"Sent IPFix template to FC {self.dest_ip}:{self.dest_port}", 'info')
        except Exception as exception:
            print(f"Error sending IPFix template: {exception}", 'error')
            return False
        try:
            self.sock.sendto(template2.to_bytes(), self.address)
            if self.DEBUG:
                print(f"Sent IPFix template to FC {self.dest_ip}:{self.dest_port}", 'info')
        except Exception as exception:
            print(f"Error sending IPFix template: {exception}", 'error')
            return False
        try:
            self.sock.sendto(template3.to_bytes(), self.address)
            if self.DEBUG:
                print(f"Sent IPFix template to FC {self.dest_ip}:{self.dest_port}", 'info')
        except Exception as exception:
            print(f"Error sending IPFix template: {exception}", 'error')
            return False
        try:
            self.sock.sendto(template4.to_bytes(), self.address)
            if self.DEBUG:
                print(f"Sent IPFix template to FC {self.dest_ip}:{self.dest_port}", 'info')
        except Exception as exception:
            print(f"Error sending IPFix template: {exception}", 'error')
            return False
        return True


    def send_record(self, record):
        validation_errors = self.validate_data_fields(record)
        if validation_errors:
            print(f'The following fields are missing from below record:\n{record}\n' + '\n'.join(validation_errors))
            return False
        forward_message = self.formulate_messages(record)
        #forward_message, reverse_message = self.formulate_messages(record)
        #if not forward_message or not reverse_message:
        #    return False
        if not forward_message:
            return False
        try:
            self.sock.sendto(forward_message.to_bytes(), self.address)
            if self.DEBUG:
                print(f"Sent IPFix record to FC {self.dest_ip}:{self.dest_port}", 'info')
        except Exception as exception:
            print(f"Error sending IPFix record: {exception}", 'error')
            return False
        # try:
        #     self.sock.sendto(reverse_message.to_bytes(), self.address)
        #     if self.DEBUG:
        #         print(f"Sent IPFix record to FC {self.dest_ip}:{self.dest_port}", 'info')
        # except Exception as exception:
        #     print(f"Error sending IPFix record: {exception}", 'error')
        #     return False
        return True


    def send_records(self, records):
        for record in records:
            self.send_record(record)

    def get_flowsensor_id(self, url):
        protocol = url.split(':')[0].lower()
        if protocol == "http":
            return 10019 # HTTP
        elif protocol == "https" or protocol == "connect":
            return 10030 # HTTPS or SSL CONNECT
        else:
            return 10226  # undefined TCP

    AVERAGE_PACKET_SIZE = 512
    INGRESS_INTERFACE = 1
    EGRESS_INTERFACE = 1
    PROTOCOL_NUMBER = 6
    CLIENT_PORT = 9999
    IP_CLASS_OF_SERVICE = 5
    TCP_CONTROL_BITS_CLN_2_SRV = 0x13
    TCP_CONTROL_BITS_SRV_2_CLN = 0x18
    MIN_TCP_EMPTY_SIZE = 21
    TCP_HEADER_SIZE = 20
    IP_HEADER_SIZE = 20
    CLN_PACKET_OFFSET = 3
    SRV_PACKET_OFFSET = 2

    def transform_data(self, data):
        # Fixup data, if not provided in data object. Transforms default or calculate values below.
        if "serverTransportPort" not in data:  # WARNING: We may eliminate this transform. It is really risky
            url_prefix = data["url"].split(':')[0]
            if url_prefix.lower() == 'https':
                data["serverTransportPort"] = 443
            else:
                data["serverTransportPort"] = 80
        if "clientPacketDeltaCount" not in data:
            packet_offset = self.CLN_PACKET_OFFSET
            data["clientPacketDeltaCount"] = (int)(
                int(data["clientOctetDeltaCount"]) / self.AVERAGE_PACKET_SIZE) + packet_offset
        if "serverPacketDeltaCount" not in data:
            packet_offset = self.SRV_PACKET_OFFSET
            data["serverPacketDeltaCount"] = (int)(
                int(data["serverOctetDeltaCount"]) / self.AVERAGE_PACKET_SIZE) + packet_offset
        if int(data["clientOctetDeltaCount"]) < self.MIN_TCP_EMPTY_SIZE:
            data["clientOctetDeltaCount"] = self.MIN_TCP_EMPTY_SIZE
        else:
            data["clientOctetDeltaCount"] = int(data["clientOctetDeltaCount"])+ ( (self.TCP_HEADER_SIZE + self.IP_HEADER_SIZE) * int(data["clientPacketDeltaCount"]) )
        if int(data["serverOctetDeltaCount"]) < self.MIN_TCP_EMPTY_SIZE:
            data["serverOctetDeltaCount"] = self.MIN_TCP_EMPTY_SIZE
        else:
            data["serverOctetDeltaCount"] = int(data["serverOctetDeltaCount"]) + ( (self.TCP_HEADER_SIZE + self.IP_HEADER_SIZE) * int(data["serverPacketDeltaCount"]) )
        if "flowSensorApplicationID" not in data:
            data["flowSensorApplicationID"] = self.get_flowsensor_id(data['url'])
        if "userName" not in data:
            data["userName"] = ""
        if "clientTransportPort" not in data:
            data["clientTransportPort"] = self.CLIENT_PORT
        if "flowStartMilliseconds" not in data:
            data["flowStartMilliseconds"] = int(data['flowEndMilliseconds']) - int(data['durationMilliseconds'])
        # ??? Some proxy mods do the extrapolation to as accurate of time as possible. How to account for that.
        if "ingressInterface" not in data:
            data['ingressInterface'] = self.INGRESS_INTERFACE
        if "egressInterface" not in data:
            data["egressInterface"] = self.EGRESS_INTERFACE
        if "protocolIdentifier" not in data:
            data["protocolIdentifier"] = self.PROTOCOL_NUMBER
        if "ipClassOfService" not in data:
            data["ipClassOfService"] = self.IP_CLASS_OF_SERVICE
        if "ingressInterface" not in data:
            data["ingressInterface"] = self.INGRESS_INTERFACE
        if "egressInterface" not in data:
            data["egressInterface"] = self.EGRESS_INTERFACE
        if "protocolIdentifier" not in data:
            data["protocolIdentifier"] = self.PROTOCOL_NUMBER


    def create_record(self, data):
        if self.DEBUG:
            print('DATA:'+str(data))

        self.transform_data(data)

        try:
            # Need to do this for the ipfix module. It needs date objects.
            flow_start_forward = datetime.datetime.fromtimestamp(int(data["flowStartMilliseconds"]) / 1000.0)
            flow_end_forward = datetime.datetime.fromtimestamp(( int(data["flowStartMilliseconds"]) + (( int(data["flowEndMilliseconds"]) - int(data["flowStartMilliseconds"]) ) / 2.0) ) / 1000.0)
            flow_start_reverse = flow_end_forward
            flow_end_reverse = datetime.datetime.fromtimestamp(int(data["flowEndMilliseconds"]) / 1000.0)
        except:
            print(traceback.format_exc())
            return None, None, None, None, None, None

        forward_record = {
            "flowStartMilliseconds": flow_start_forward,
            "flowEndMilliseconds": flow_end_forward,
            "sourceTransportPort": int(data['clientTransportPort']),
            "destinationTransportPort": int(data['serverTransportPort']),
            "octetDeltaCount": int(data['clientOctetDeltaCount']),
            "packetDeltaCount": int(data['clientPacketDeltaCount']),
            "ingressInterface": int(data['ingressInterface']),
            "egressInterface": int(data['egressInterface']),
            "protocolIdentifier": int(data['protocolIdentifier']),
            "tcpControlBits": self.TCP_CONTROL_BITS_CLN_2_SRV,
            "ipClassOfService": int(data['ipClassOfService']),
            "flowSensorApplicationID": int(data['flowSensorApplicationID']),
            "flowSensorApplicationDetails": f'{data["method"]} {data["url"]}',
            "userName": data['userName']}

        reverse_record = dict(forward_record)
        reverse_record["tcpControlBits"] = self.TCP_CONTROL_BITS_SRV_2_CLN
        reverse_record["flowStartMilliseconds"] = flow_start_reverse
        reverse_record["flowEndMilliseconds"] = flow_end_reverse
        reverse_record["octetDeltaCount"] = int(data['serverOctetDeltaCount'])
        reverse_record["packetDeltaCount"] = int(data['serverPacketDeltaCount'])
        reverse_record['sourceTransportPort'] = forward_record['destinationTransportPort']
        reverse_record['destinationTransportPort'] = forward_record['sourceTransportPort']
        forward_template = self.template_4_4
        forward_template_id = self.template_id_4_4
        reverse_template = self.template_4_4
        reverse_template_id = self.template_id_4_4
        if type(ipaddress.ip_address(data['clientIPAddress'])) is IPv4Address and type(ipaddress.ip_address(data['serverIPAddress'])) is IPv4Address:
            forward_template = self.template_4_4
            forward_template_id = self.template_id_4_4
            reverse_template = self.template_4_4
            reverse_template_id = self.template_id_4_4
            forward_record["sourceIPv4Address"] = ipaddress.ip_address(data['clientIPAddress'])
            forward_record["destinationIPv4Address"] = ipaddress.ip_address(data['serverIPAddress'])
            reverse_record["sourceIPv4Address"] = ipaddress.ip_address(data['serverIPAddress'])
            reverse_record["destinationIPv4Address"] = ipaddress.ip_address(data['clientIPAddress'])
        elif type(ipaddress.ip_address(data['clientIPAddress'])) is IPv4Address and type(ipaddress.ip_address(data['serverIPAddress'])) is IPv6Address:
            forward_template = self.template_4_6
            forward_template_id = self.template_id_4_6
            forward_record["sourceIPv4Address"] = ipaddress.ip_address(data['clientIPAddress'])
            forward_record["destinationIPv6Address"] = ipaddress.ip_address(data['serverIPAddress'])
            # SWAPPED FORCE USE 6_4 template on reverse
            reverse_template = self.template_6_4
            reverse_template_id = self.template_id_6_4
            reverse_record["sourceIPv6Address"] = ipaddress.ip_address(data['serverIPAddress'])
            reverse_record["destinationIPv4Address"] = ipaddress.ip_address(data['clientIPAddress'])
        elif type(ipaddress.ip_address(data['clientIPAddress'])) is IPv6Address and type(ipaddress.ip_address(data['serverIPAddress'])) is IPv4Address:
            forward_template = self.template_6_4
            forward_template_id = self.template_id_6_4
            # SWAPPED FORCE USE 4_6 template on reverse
            reverse_template = self.template_4_6
            reverse_template_id = self.template_id_4_6
            forward_record["sourceIPv6Address"] = ipaddress.ip_address(data['clientIPAddress'])
            forward_record["destinationIPv4Address"] = ipaddress.ip_address(data['serverIPAddress'])
            reverse_record["sourceIPv4Address"] = ipaddress.ip_address(data['serverIPAddress'])
            reverse_record["destinationIPv6Address"] = ipaddress.ip_address(data['clientIPAddress'])
        elif type(ipaddress.ip_address(data['clientIPAddress'])) is IPv6Address and type(ipaddress.ip_address(data['serverIPAddress'])) is IPv6Address:
            forward_template = self.template_6_6
            forward_template_id = self.template_id_6_6
            reverse_template = self.template_6_6
            reverse_template_id = self.template_id_6_6
            forward_record["sourceIPv6Address"] = ipaddress.ip_address(data['clientIPAddress'])
            forward_record["destinationIPv6Address"] = ipaddress.ip_address(data['serverIPAddress'])
            reverse_record["sourceIPv6Address"] = ipaddress.ip_address(data['serverIPAddress'])
            reverse_record["destinationIPv6Address"] = ipaddress.ip_address(data['clientIPAddress'])

        if self.DEBUG:
            print('FWD:'+str(forward_record))

        response_code = data['responseCode']
        if response_code in self.HTTP_CODES:
            response_text = self.HTTP_CODES[response_code]
        else:
            response_text = ''
        reverse_record['flowSensorApplicationDetails'] = f"{response_code} {response_text}"
        if self.DEBUG:
            print('REV:'+str(reverse_record))
        return forward_record, reverse_record, forward_template, forward_template_id, reverse_template, reverse_template_id


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: test_ipfix.py <destination address> <destination port> <message_file>")
        print("NOTE: Message file contains single line json objects representing the IPFix data to be sent via the default template.")
        sys.exit(1)
    ipfix_sender = IPFix(sys.argv[1], int(sys.argv[2]))
    ipfix_sender.send_templates()
    with open(sys.argv[3]) as messages_fd:
        for index, line in enumerate(messages_fd):
            if line.strip("\n") == '':
                continue
            data = json.loads(line.strip().strip("\n"))
            data['flowEndMilliseconds'] = f'{int(datetime.datetime.utcnow().timestamp()*1000)}'
            if not ipfix_sender.send_record(data):
                print(f"Failure sending data on line #{index+1}")
                sys.exit(1)
    sys.exit(0)
