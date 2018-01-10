import socket
import struct
import configparser
import threading
import logging.config
import os
import json


class FTPServerConfig(object):

    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))

    def __init__(self, config_file="FTPServer/server_config.ini",logger_config_file="FTPServer/logger_config.json"):

        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(config_file)

        if os.path.exists(logger_config_file):

                with open(logger_config_file, "rt") as cfg:
                        logging.config.dictConfig(json.load(cfg))
        else:
            logging.basicConfig(level=logging.INFO)

    def getDefaultFolder(self):
        return self.config_parser.get("ftpsrvconfig","folder")

    def getConfigPort(self):
        return int(self.config_parser.get("ftpsrvconfig","port"))

    def getDefaultHostAddress(self):
        return self.config_parser.get("ftpsrvconfig", "hostaddress")

class ThreadFTPClientHandler(threading.Thread):


    def __init__(self):
        pass

    def run(self):
        pass


class FTPServer(object):

    MAX_SEND_BYTES = 1024

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

    def shutdown_server(self):
        self.server_logger.info("Server is closing...")
        self.server_active = False
        self.server_socket.close()
