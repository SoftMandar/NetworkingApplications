import socket
import struct
import threading
import logging.config
import subprocess
import os
import pickle

from config.config import FTPServerConfig

class ThreadFTPClientHandler(threading.Thread):

    MAX_RECV_BYTES = 1430
    MAX_SEND_BYTES = 1440
    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, client_socket, client_address):

        super(ThreadFTPClientHandler,self).__init__()

        self.client_sock = client_socket
        self.client_addr = client_address

        self.sys_commands = ["ls -l", "ls", "rm", "rm -r"]
        self.tcp_commads = ['-d', '-e']

    def run(self):

        #data_buf = self.client_sock.recv(ThreadFTPClientHandler.MAX_RECV_BYTES)
        data_buffer = ""

        while True:

            clt_data = self.client_sock.recv(ThreadFTPClientHandler.MAX_RECV_BYTES)
            if not clt_data:
                print("Client just disconnected...")
                break

            data_buffer+=clt_data.decode("utf-8")
            command_args = data_buffer.split(" ")
            if command_args[0] in self.sys_commands:

                self.proceed_command(data_buffer)
            elif command_args[0] in self.tcp_commads:
                if command_args[0] == "-d":
                    self.download_file(command_args[1])
                else:
                    self.download_folder(command_args[1])

            else:
                self.client_sock.send("Command is nor reconized".encode("utf-8"))
            data_buffer = ""


    def download_file(self, filename):
        file_path = "%s/%s" % (ThreadFTPClientHandler.BASE_FOLDER,filename)
        if os.path.exists(file_path):

            file_size = os.path.getsize(file_path)
            packer = struct.Struct('I')
            packet_data = packer.pack(file_size)

            try:

                self.client_sock.send(packet_data)

                with open(file_path, "rb") as df:
                    data = 0
                    while data <= file_size:
                        self.client_sock.send(df.read(ThreadFTPClientHandler.MAX_SEND_BYTES))
                        data+=ThreadFTPClientHandler.MAX_SEND_BYTES
            except IOError as ierr:
                sys.exit(1)

        else:
            self.client_sock.send("No such file".encode("utf-8"))

    def download_folder(self, foldername):
        folder_path = "%s/%s" % (ThreadFTPClientHandler.BASE_FOLDER,foldername)

        if os.path.exists(folder_path):
            folder_files = ["%s/%s" % (foldername,f) for f in os.listdir(folder_path)]
            self.client_sock.send(pickle.dumps(folder_files))
            for f in folder_files:
                    self.download_file(f)
        else:
            self.client_sock.send("No such folder".encode("utf-8"))


    def delete_file(self, filename):
        file_path = "%s/%s" % (ThreadFTPClientHandler.BASE_FOLDER,filename)
        if os.path.exists(file_path):
            try:
                subprocess.call(['rm' , file_path], stderr=subprocess.STDOUT,shell=True)
            except OSError as ierr:
                str_err = str(ierr)

                if str_err.find("Permission denied"):
                    self.client_sock.send("[Errno 13] Permission denied".encode("utf-8"))

        else:
            self.client_sock.send("No such file".encode("utf-8"))


    def delete_folder(self, foldername):

        if os.path.exists(filename):
                try:
                    subprocess.call(['rm' , '-r', foldername], stderr=subprocess.STDOUT,shell=True)
                except OSError as ierr:
                    str_err = str(ierr)

                    if str_err.find("Permission denied"):
                        self.client_sock.send("[Errno 13] Permission denied".encode("utf-8"))
        else:
            self.client_sock.send("No such folder".encode("utf-8"))


    def proceed_command(self, command):
        try:
            output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
            self.client_sock.send(output)
        except OSError as oerr:
            self.client_sock.send("Failed to execute command\n".encode("utf-8"))

class FTPServer(object):

    def __init__(self, server_address=None, blocking=False, reuse_address=False, usrBacklog=1):

        self.server_logger = logging.getLogger(__name__)

        self.server_config = FTPServerConfig()
        if server_address is not None:
            self.server_address = server_address
        else:
            self.server_address = (self.server_config.getDefaultHostAddress(), self.server_config.getConfigPort())
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.bind(self.server_address)
        except socket.error as serr:
            self.server_logger.exception(serr)

        if blocking:
            self.server_socket.setblocking(1)
        if reuse_address:
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.listen(usrBacklog)
        self.server_active = True

    def start_server(self):

        self.server_logger.info("Server just started on => {}:{}".format(self.server_address[0],self.server_address[1]))
        try:
            while self.server_active:

                self.handle_request()
        except KeyboardInterrupt as kerr:
            self.shutdown_server()

    def handle_request(self):

        client_socket, client_address = self.server_socket.accept()

        self.server_logger.info("Client just connected with the address => {}:{}".format(client_address[0],client_address[1]))

        client_handler = ThreadFTPClientHandler(client_socket, client_address)
        client_handler.start()

        self.server_logger.info("Client {} started".format(client_handler.getName()))

    def shutdown_server(self):
        self.server_logger.info("Server is closing...")
        self.server_active = False
        self.server_socket.close()
