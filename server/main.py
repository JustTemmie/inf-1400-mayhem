import socket


class SharedData:
    def __init__(self):
        self.noc = 0
        self.conn = []


class Server:
    def __init__(self):
        pass

    def start(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind(("", 27827))
        while True:
            message, addr = self.serverSocket.recvfrom(1024)
            self.serverSocket.sendto(message, addr)


if __name__ == "__main__":
    server = Server()
    server.start()
