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
                self.client_socket.close()
                print(serr)
        else:
                self.connected = True

        try:
            while self.connected:

                if self.server_address[0] == "127.0.0.1":
                    command = input("\nlocalhost@localhost" + ">> ")
                else:
                    command = input(self.server_address[0] +'@' + self.server_address +">> \n")

                self.client_socket.send(command.encode("utf-8"))

                recv_length = 1

                data_buffer = ""

                while recv_length:
                    recv_data = self.client_socket.recv(TCPClient.MAX_RECV_BYTES)
                    print(recv_data.decode("utf-8").strip())
                    recv_length = len(recv_data)

                    if not recv_data:
                        break

                    elif recv_length < TCPClient.MAX_RECV_BYTES:
                        break

                    data_buffer+=recv_data

                data_buffer = ""

        except IOError as ierr:
            print("An error accoured while io operation")
            self.connected = False
            self.client_socket.close()
            sys.exit()

        except KeyboardInterrupt as kerr:
            print("Clossing connection...")
            self.client_socket.close()
            sys.exit()

client = TCPClient(("127.0.0.1",8080))
client.connect_to_server()
