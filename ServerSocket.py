import socket
from threading import Thread

class ClientHandler(object):

        def __init__(self):
            pass

        def handle_client(self):
            pass


class TCPServer(object):

    def __init__(self, server_address, blocking=False, reuse_address=False, usrBackLog=5):
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(server_address)
        if reuse_address:
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT")
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socket.listen(usrBackLog)

    def start_server(self):
        pass


class UDPServer(object):
        pass

class ThreadingTCPServer(object):
        pass

class ThreadingUDPpServer(object):
        pass
