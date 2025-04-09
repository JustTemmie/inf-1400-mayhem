"""
The server sided code
@author: Benjamin
"""

# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!

if __name__ == "__main__":
    import sys

    sys.path.append(".")

import socket
from server.player import Player


class Server:
    """
    The server class.
    Will listen for updates from players and relay their information to the other players.
    Will also give each player an id.
    """

    def __init__(self):
        self.clients = {}
        self.player_ids = []

    @staticmethod
    def encode(data: tuple):
        """
        Encodes the data from a tuple to bytes.

        Parameters:
            data (tuple): The data you want to encode

        Returns:
            bytes: The encoded data
        """
        out = ""
        for i in data:
            out += f" {str(i)}"
        return out[1:].encode()

    def start(self):
        """
        Startes the server.
        Starts an UDP server to relay messages between players.
        """
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverSocket.bind(("", 27827))
        print("Server started on port:", 27827)

        while True:
            data, addr = self.serverSocket.recvfrom(1024)
            decoded_data = list(data.decode().split(" "))
            """
            How the data is formated (Porbably under 1 KB):

            0, 1        --- player/server ids (from, to)

            2, 3, 4     --- client pos (x, y, z)
            5, 6, 7     --- client velocity (x, y, z)
            8, 9, 10    --- client acceleration (x, y, z)

            11, 12, 13  --- client rotation (x, y, z)
            14, 15, 16  --- client rotation speed (x, y, z)
            17, 18, 19  --- client rotation acceleration (x, y, z)

            20          --- new bullet? If 0 no new bullet

            21          --- Killed by player id (if zero not killed)
            """

            if addr not in self.clients:
                if len(self.player_ids) == 0:
                    new_player_id = 1
                else:
                    new_player_id = self.player_ids[-1] + 1

                self.player_ids.append(new_player_id)
                new_player = Player(addr, new_player_id)
                self.clients[addr] = new_player

            for client in self.clients.values():
                packet = decoded_data
                packet[0] = self.clients[addr].player_id
                packet[1] = client.player_id

                if client != self.clients[addr]:
                    self.serverSocket.sendto(self.encode(packet), client.addr)


if __name__ == "__main__":
    s = Server()
    s.start()
