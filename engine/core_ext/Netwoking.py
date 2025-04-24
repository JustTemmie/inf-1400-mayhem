"""
Contains the Networking class.
Authors: BAaboe (i'll replace names at handin)
"""

import socket
from threading import Thread, Lock
import queue
import time
import logging


class Networking:
    """
    Very simple networking class.
    """

    def __init__(self, port: int, addr: str):
        """
        Creates and connects a socket to the given addreee.
        Also creates a queue with all the new requsts.
        Parameters:
            port: The port
            addr: The IPv4 address to connect to
        """
        self.port = port
        self.addr = addr

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.connect((self.addr, self.port))

        self.connected = True

        self.q = queue.Queue()
        self.lock = Lock()

    def send(self, data: bytes):
        """
        Sends the given data on the socket
        Parameters:
            data: The data to send
        """
        try:
            self.s.send(data.encode())
        except ConnectionRefusedError:
            self.connected = False
            logging.warning("No connection to server")

    @staticmethod
    def _listen(self):
        """
        Waits for a requst and adds it to the queue.
        """
        while not self.connected:
            time.sleep(1)
        while True:
            try:
                data = self.s.recv(1024)

                # Makes sure that only one thread accesses the queue at the time
                self.lock.acquire()
                self.q.put(data)
                self.lock.release()
            except ConnectionRefusedError:
                self.connected = False
                logging.warn(f"Could not connect to server {self.addr}, playing localy")

    def start_listen(self):
        """
        Starts a new thread that will just listen
        """
        thread = Thread(target=self._listen, args=(self,))
        thread.start()
