import sys
import os
import socket
import struct
import subprocess
import errno
import pickle

class TCPClient(object):

    MAX_RECV_BYTES = 1440
    DOWNLOAD_LOCATION = os.path.dirname(os.path.abspath(__file__)) + "/Downloads"

    def __init__(self,server_address, download_folder=None):

        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.commands = ["-d", "-e"]

        if download_folder:
            self.download_location = download_folder
        else:
            self.download_location = TCPClient.DOWNLOAD_LOCATION

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
                args = command.split(" ")
                if args[0] in self.commands:
                    if args[0] == "-d":
                        self.download_file(args[1])
                    elif args[0] == "-e":
                        self.download_folder(args[1])
                else:

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
            sys.exit(1)

        except KeyboardInterrupt as kerr:
            print("Clossing connection...")
            self.client_socket.close()
            sys.exit(0)

    def download_file(self, filename):
        unpacker = struct.Struct('I')
        file_length = unpacker.unpack(self.client_socket.recv(unpacker.size))[0]
        if os.path.exists(self.download_location):
            file_location = "%s/%s" % (TCPClient.DOWNLOAD_LOCATION,filename)
            with open(file_location, "wb") as df:
                print("File location for {}: {} was created".format(filename,file_location))

                recv_len = 0
                try:
                    while recv_len < file_length:
                        file_data = self.client_socket.recv(TCPClient.MAX_RECV_BYTES)
                        df.write(file_data)
                        recv_len += len(file_data)
                except IOError as ioerr:
                        sys.exit(1)

                print("File: {} Bytes: {} was succesfuly downloaded".format(filename, file_length))
        else:
            print("[ERROR]: Storage download location dosen't exist")
            sys.exit(1)

    def download_folder(self,foldername):
        folder_location = "%s/%s" % (TCPClient.DOWNLOAD_LOCATION,foldername)
        try:
            data_buffer = self.client_socket.recv(TCPClient.MAX_RECV_BYTES)
            print(data_buffer)
            list_files = pickle.loads(data_buffer)
            for f in list_files:
                self.download_file(f)

        except OSError as oerr:
            if oerr.errno == errno.EEXIST:
                print("[ERROR]: File already exists")

client = TCPClient(("127.0.0.1",8080))
client.connect_to_server()
