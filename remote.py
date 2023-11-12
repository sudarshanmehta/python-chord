import json
import socket
import threading
from address import Address
from settings import SIZE
from network import read_from_socket

# Decorator to make Remote's socket thread-safe
def requires_connection(func):
    """ Initiates and cleans up connections with a remote server """
    def inner(self, *args, **kwargs):
        self.mutex_.acquire()

        self.open_connection()
        ret = func(self, *args, **kwargs)
        self.close_connection()
        self.mutex_.release()

        return ret

    return inner

# Class representing a remote peer
class Remote:
    def __init__(self, remote_address):
        self.address_ = remote_address
        self.mutex_ = threading.Lock()
        self.socket_ = None

    def open_connection(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.connect((self.address_.ip, self.address_.port))

    def close_connection(self):
        if self.socket_:
            self.socket_.close()
            self.socket_ = None

    def __str__(self):
        return "Remote %s" % self.address_

    def id(self, offset=0):
        return (self.address_.__hash__() + offset) % SIZE

    def send(self, msg):
        if self.socket_:
            self.socket_.sendall((msg + "\r\n").encode())  # Encode the message to bytes
            self.last_msg_send_ = msg

    def recv(self):
        if self.socket_:
           return read_from_socket(self.socket_)
        return ""

    def ping(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.address_.ip, self.address_.port))
            s.sendall(b"\r\n")
            s.close()
            return True
        except socket.error:
            return False

    @requires_connection
    def command(self, msg):
        self.send(msg)
        response = self.recv()
        return response

    @requires_connection
    def get_successors(self):
        self.send('get_successors')

        response = self.recv()
        if response == "":
            return []

        response = json.loads(response)
        return [Remote(Address(address[0], address[1])) for address in response]

    @requires_connection
    def successor(self):
        self.send('get_successor')

        response = json.loads(self.recv())
        return Remote(Address(response[0], response[1]))

    @requires_connection
    def predecessor(self):
        self.send('get_predecessor')

        response = self.recv()
        if response == "":
            return None

        response = json.loads(response)
        return Remote(Address(response[0], response[1]))

    @requires_connection
    def find_successor(self, id):
        self.send('find_successor %s' % id)

        response = json.loads(self.recv())
        return Remote(Address(response[0], response[1]))

    @requires_connection
    def closest_preceding_finger(self, id):
        self.send('closest_preceding_finger %s' % id)

        response = json.loads(self.recv())
        return Remote(Address(response[0], response[1]))

    @requires_connection
    def notify(self, node):
        self.send('notify %s %s' % (node.address_.ip, node.address_.port))
