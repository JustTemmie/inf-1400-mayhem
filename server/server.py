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
import time
import config_server


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

            21          --- Killed by player id (if negativ not killed)
            """

            if addr not in self.clients:
                if len(self.player_ids) == 0:
                    new_player_id = 1
                else:
                    new_player_id = self.player_ids[-1] + 1

                self.player_ids.append(new_player_id)
                new_player = Player(addr, new_player_id, time.time())
                self.clients[addr] = new_player
                print(f"Player from {addr} joined. Given the ID {new_player_id}")

            self.clients[addr].time_last_message = time.time()
            self.broadcast(decoded_data, self.clients[addr])

    def broadcast(self, packet, client_from=None):
        """
        Broadcasts a message to all clients

        Parameters:
            packet: The packet to broadcacst
            client_from: Who sent the message
        """
        timeout_clients = []
        for client in self.clients.values():
            # Check out if the client has timedout
            if time.time()-client.time_last_message > config_server.SERVER_TIMEOUT:
                timeout_clients.append(client)
                client.time_last_message = time.time() # Making sure that it will not be flaged when the timeout message get broadcasted
                continue

            if client != client_from:
                # Send packet to client
                if client_from:
                    packet[0] = client_from.player_id
                else:
                    packet[0] = 0
                packet[1] = client.player_id
                self.serverSocket.sendto(self.encode(packet), client.addr)

        # Tell the other clients that the player has disconnected
        for client in timeout_clients:
            print(f"Player from {client.addr} with ID {client.player_id} timedout")
            self.clients.pop(client.addr)
            self.player_ids.remove(client.player_id)
            packet = [0]*22

            self.broadcast(packet, client)





if __name__ == "__main__":
    s = Server()
    s.start()
