import socket

def attempt_connection():
    # Create a UDP socket
    outSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    respSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Bind the socket to a specific port
    respSock.bind(('0.0.0.0', 1819))

    # Enable broadcasting mode
    outSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send the ping to all devices on port 1818
    outSock.sendto(b'ping', ('<broadcast>', 1818))

    outSock.close()

    # Set a timeout of 5 seconds
    respSock.settimeout(1)

    address = None

    try:
        # Receive the response
        data, addr = respSock.recvfrom(1024)
        address = addr[0]
    except socket.timeout:
        pass

    # Close the socket
    respSock.close()
    
    return address


def get_server():
    print('Connecting to maestro')
    while True:
        addr = attempt_connection()
        if addr is not None:
            print('Connected to maestro at ' + addr)
            return addr
