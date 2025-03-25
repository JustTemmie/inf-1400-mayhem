import socket
import abc
import threading
import queue


class Networking(abc.ABC):
    def __init__(self, port: int, addr: str):
        self.port = port
        self.addr = addr

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.connect((self.addr, self.port))
        self.s.send(b"1 1 1")

        self.q = queue.Queue()

    def send(self, data):
        self.s.send(self.encode(data))

    @staticmethod
    def _listen(self, s: socket.socket, q: queue.Queue):
        while True:
            data = self.decode(s.recv(1024))
            print(data)
            q.put(data)

    def start_listen(self):
        thread = threading.Thread(target=self._listen, args=(self, self.s, self.q, ))
        thread.start()

    @abc.abstractmethod
    def encode(self, data):
        pass

    @abc.abstractmethod
    def decode(self, data):
        pass


class TestNetworking(Networking):
    """Test class, do not use outside of this file"""

    def encode(self, data: tuple):
        out = ""
        for i in data:
            out += f" {i}"
        return out[1:].encode()

    def decode(self, data):
        return tuple(data.decode().split(" "))


if __name__ == "__main__":
    n = TestNetworking(27827, "127.0.0.1")
    n.start_listen()
