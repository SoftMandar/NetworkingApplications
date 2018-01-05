import socket
from threading import Thread

class ClientHandler(object):

        def __init__(self):
            pass

        def handle_client(self):
            pass


class TCPServer(object):


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

        print("Server just started on -> {}:{}".format(self.server_address[0],self.server_address[1]))

        try:

            while self.serverIsUp:

                client_sock,client_addr = self.server_socket.accept()

                print("Client just connected with address -> {}:{}".format(client_addr[0],client_addr[1]))

                client_sock.send("Hello you've just connected".encode("utf-8"))

        except KeyboardInterrupt as kerr:
            print("\nClosing server...")
            self.shutdown_server()

    def shutdown_server(self):

        self.serverIsUp = False
        self.server_socket.close()



class UDPServer(object):

        MAX_RECV_BUFFER = 1450

        def __init__(self, server_address, blocking=False, reuse_address=False, usrBackLog=1):

            self.server_address = server_address
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




class ThreadingTCPServer(object):
        pass

class ThreadingUDPpServer(object):
        pass
