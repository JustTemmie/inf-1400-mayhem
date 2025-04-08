import socket
import abc
from threading import Thread, Lock
import queue
import time


class Networking(abc.ABC):
    def __init__(self, port: int, addr: str):
        self.port = port
        self.addr = addr

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.connect((self.addr, self.port))

        self.connected = True

        self.q = queue.Queue()
        self.lock = Lock()

    def send(self, data):
        try:
            self.s.send(data.encode())
        except ConnectionRefusedError:
            self.connected = False
            print("No connection to server")

    @staticmethod
    def _listen(self):
        while not self.connected:
            time.sleep(1)
        while True:
            try:
                data = self.s.recv(1024)

                self.lock.acquire()
                self.q.put(data)
                self.lock.release()
            except ConnectionRefusedError:
                self.connected = False

    def start_listen(self):
        thread = Thread(target=self._listen, args=(self,))
        thread.start()
