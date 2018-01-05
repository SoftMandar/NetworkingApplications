import socket



class TCPClient(object):

    MAX_RECV_BUFFER = 1450

    def __init__(self, server_address):

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = server_address

    def connect_to_server(self):

        self.client_sock.connect(self.server_address)

        print("Connecting...")

        data = self.client_sock.recv(TCPClient.MAX_RECV_BUFFER)

        if data:

            print("You've just coonected to -> {}:{}".format(self.server_address[0],self.server_address[1]))
            print("Server replied: {}".format(data.decode("utf-8")))

        self.client_sock.close()

class UDPClient(object):

    MAX_RECV_BUFFER = 1450

    def __init__(self, server_address):

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = server_address

    def send_to_server(self):

        self.client_sock.sendto("I've just conneted to your server".encode("utf-8"),(self.server_address[0],self.server_address[1]))

        data,serveraddr = self.client_sock.recvfrom(UDPClient.MAX_RECV_BUFFER)

        print("I've just recieved {} bytes from server: {}".format(len(data), data.decode("utf-8")))

        self.client_sock.close()


if __name__ == "__main__":
    client = UDPClient(("127.0.0.1",8080))
    client.send_to_server()
