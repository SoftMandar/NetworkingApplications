import sys
import socket
import struct

class TCPClient(object):

    MAX_RECV_BYTES = 1440

    def __init__(self,server_address):

        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect_to_server(self):

        try:
                self.client_socket.connect(self.server_address)
        except socket.error as serr:
                sys.stderr.write(serr)
        else:
                self.connected = True

        while self.connected:

            self.client_socket.send(command.encode("utf-8"))
