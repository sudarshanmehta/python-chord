import socket
import sys

def send_message(server_address, server_port, message):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        server_address = (server_address, server_port)
        client_socket.connect(server_address)

        # Send data
        client_socket.send(message.encode() + b"\r\n")
        print('Message sent:', message)
        # print(client_socket.recv(1000).decode())

    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    # Check if enough command-line arguments are provided
    # if len(sys.argv) != 4:
    #     print("Usage: python client.py <server_address> <server_port> <message>")
    #     sys.exit(1)

    # Extract command-line arguments
    server_address = "127.0.0.1"
    server_port = 46924
    message = "Command: whoami"

    # Call the function to send the message
    while True:
        command = input("Command: ")   
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_address, server_port))
        s.sendall(command.encode() + b"\r\n")
        print("Response : '%s'" % s.recv(10000).decode())
        s.close()
    # send_message(server_address, server_port, message)
