import socket


"""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('10.254.162.85', 2055)
message = b'This is the test data'

try:
    print(f'Sending {message} to {server_address[0]} port {server_address[1]}')
    sent = sock.sendto(message, server_address)
    print(sent)
finally:
    print('Closing socket')
    sock.close()
"""

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a server
s.connect(('10.254.162.85', 2055))  # replace with your server IP and port

# Create a message to send
message = "Hello, Server!"

# Send the message
bytes_sent = s.send(message.encode())  # encode string to bytes

# Print the number of bytes sent
print(f"Sent {bytes_sent} bytes.")