import socket
import threading
import struct

class BaseTCPServer(object):

    def __init__(self, server_address, blocking=False, reuse_address=False, usrBackLog=5):
        self.server_address= server_address
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(server_address)
        if reuse_address:
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if hasattr(socket, "SO_REUSEPORT"):
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        if blocking:
            self.server_socket.setblocking(1)
        self.server_socket.listen(usrBackLog)
        self.serverIsUp = True


    def start_server(self):
        raise NotImplemented("Must be implemented in subclass")

    def handle(self):
        raise NotImplemented("Must e implemented in subclass")

    def shutdown_server(self):
        raise NotImplemented("Must be implementd in subclass")


class BaseUDPServer(object):

        def __init__(self, server_address, blocking=False, reuse_address=False, usrBackLog=5):
            self.server_address= server_address
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind(server_address)
            if reuse_address:
                self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if hasattr(socket, "SO_REUSEPORT"):
                    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            if blocking:
                self.server_socket.setblocking(1)
            self.serverIsUp = True


        def start_server(self):
            raise NotImplemented("Must be implemented in subclass")

        def handle(self):
            raise NotImplemented("Must e implemented in subclass")

        def shutdown_server(self):
            raise NotImplemented("Must be implementd in subclass")

class ThreadTCPClientHandler(threading.Thread):

        def __init__(self, client_socket, client_addr):
            super(ThreadTCPClientHandler,self).__init__()
            self.client_socket = client_socket
            self.client_addr = client_addr

        def run(self):

            print("Client just connected with address -> {}:{}".format(self.client_addr[0],self.client_addr[1]))

            self.client_socket.send("Hello you've just connected".encode("utf-8"))

class ThreadUDPClientHandler(object):

    def __init__(self, data , client_addr, server_socket):
        super(ThreadUDPClientHandler,self).__init__()
        self.client_data = data
        self.client_addr = client_addr
        self.server_socket = server_socket

    def run():

        print("Just recieved {} bytes from -> {}:{} ".format(len(self.data), self.client_addr[0],self.client_addr[1]))

        self.server_socket.sendto("Hello you've just connected".encode("utf-8"), (self.client_addr[0],self.client_addr[1]))


class TCPServer(BaseTCPServer):

    def start_server(self):

        print("Server just started on -> {}:{}".format(self.server_address[0],self.server_address[1]))

        try:

            while self.serverIsUp:
                self.handle()

        except KeyboardInterrupt as kerr:
            print("\nClosing server...")
            self.shutdown_server()

    def handle(self):

        client_sock,client_addr = self.server_socket.accept()

        print("Client just connected with address -> {}:{}".format(client_addr[0],client_addr[1]))

        client_sock.send("Hello you've just connected".encode("utf-8"))

    def shutdown_server(self):

        self.serverIsUp = False
        self.server_socket.close()



class UDPServer(BaseUDPServer):

        MAX_RECV_BUFFER = 1450

        def start_server(self):

            self.handle()

        def handle(self):

                print("Server just started on -> {}:{}".format(self.server_address[0],self.server_address[1]))

                try:
                        while self.serverIsUp:

                            data,client_addr = self.server_socket.recvfrom(UDPServer.MAX_RECV_BUFFER)

                            print("Just recieved {} bytes from -> {}:{} ".format(len(data), client_addr[0],client_addr[1]))

                            self.server_socket.sendto("Hello you've just connected".encode("utf-8"), (client_addr[0],client_addr[1]))



                except KeyboardInterrupt as kerr:
                        print("\n Closing server...")
                        self.shutdown_server()

        def shutdown_server(self):

            self.serverIsUp = False
            self.server_socket.close()




class ThreadingTCPServer(BaseTCPServer):

    def start_server(self):

        print("Server just started on -> {}:{}".format(self.server_address[0],self.server_address[1]))

        try:

            while self.serverIsUp:
                self.handle()

        except KeyboardInterrupt as kerr:
            print("\nClosing server...")
            self.shutdown_server()

    def handle(self):

        client_sock,client_addr = self.server_socket.accept()

        client_handler = ThreadTCPClientHandler(client_sock, client_addr)

        client_handler.start()

    def shutdown_server(self):

        self.serverIsUp = False
        self.server_socket.close()



class ThreadingUDPServer(BaseUDPServer):

        MAX_RECV_BUFFER = 1450

        def start_server(self):

            print("Server just started on -> {}:{}".format(self.server_address[0],self.server_address[1]))
            self.handle()

        def handle(self):
                try:
                    while self.serverIsUp:
                        data,client_addr = self.server_socket.recvfrom(UDPServer.MAX_RECV_BUFFER)
                        client_handler = ThreadUDPClientHandler(data, client_addr)
                        client_handler.start()

                except KeyboardInterrupt as kerr:
                        print("\n Closing server...")
                        self.shutdown_server()

        def shutdown_server(self):

            self.serverIsUp = False
            self.server_socket.close()
