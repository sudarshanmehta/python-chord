# Reads from the socket until "\r\n"
def read_from_socket(s):
    result = b""  # Initialize result as bytes
    while True:
        data = s.recv(256)
        if data[-2:] == b"\r\n":
            result += data[:-2]
            break
        result += data
    return result.decode('utf-8')  # Decode the received data from bytes to string

# Sends data on the socket, adding "\r\n"
def send_to_socket(s, msg):
    s.sendall((msg + "\r\n").encode('utf-8'))  # Encode the message to bytes and send it
