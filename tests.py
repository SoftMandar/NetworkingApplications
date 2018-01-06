from ServerSocket import ThreadingUDPServer

if __name__ == "__main__":
    server =  ThreadingUDPServer(("127.0.0.1",8080),reuse_address=True)
    server.start_server()
