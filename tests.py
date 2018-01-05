from ServerSocket import TCPServer,UDPServer

if __name__ == "__main__":
    server = UDPServer(("127.0.0.1",8080),reuse_address=True)
    server.start_server()
