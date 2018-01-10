import struct
import configparser
import threading


class FTPServerConfig(object):


    def __init__(self, config_file):

        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(config_file)
        print(self.config_parser.sections())

    def getDefaultFolder(self):
        return self.config_parser.get("ftpsrvconfig","folder")

    def getConfigPort(self):
        return self.config_parser.get("ftpsrvconfig","port")

    def getDefaultHostAddress(self):
        return self.config_parser.get("ftpsrvconfig", "hostaddress")

class ThreadFTPClientHandler(threading.Thread):
    pass


class FTPServer(object):

    MAX_SEND_BYTES = 1024

    def __init__(self):
        pass

    def start_server(self):
        pass

    def handle(self):
        pass

    def shutdown_server(self):
        pass
