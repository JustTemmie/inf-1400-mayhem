import socket
import abc
from threading import Thread, Lock
import queue


class Networking(abc.ABC):
    def __init__(self, port: int, addr: str):
        self.port = port
        self.addr = addr

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.connect((self.addr, self.port))

        self.connected = True

        self.s.send(b"1 1 1")

        self.q = queue.Queue()
        self.lock = Lock()

    def send(self, data):
        try:
            self.s.send(self.encode(data))
        except ConnectionRefusedError:
            self.connected = False
            print("No connection to server")

    @staticmethod
    def _listen(s: socket.socket, q: queue.Queue, lock: Lock):
        while True:
            data = s.recv(1024)

            lock.acquire()
            q.put(data)
            lock.release()

    def start_listen(self):
        thread = Thread(target=self._listen, args=(self.s, self.q, self.lock,))
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
