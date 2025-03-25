import socket
from player import Player


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

        while True:
            data, addr = self.serverSocket.recvfrom(1024)
            decoded_data = tuple(data.decode().split(" "))
            """
            How the data is formated (Porbably under 1 KB):

            0, 1, 2     --- client pos (x, y, z)
            3, 4, 5     --- client yaw, pitch, roll
            4, 5, 6     --- client velocity in spheric cordinates (yaw, pitch, speed)
            7           --- client roll speed
            8, 9, 10    --- client acceleration in spheric cordinates (yaw, pitch, speed)
            11          --- client roll acceleration

            12, 13, 14  --- new bullet pos (x, y, z) (If zero, no new bullet)
            15, 16, 17  --- new bullet yaw, pitch, roll
            18, 19, 20  --- new bullet velocity in spheric cordinates (yaw, pitch, speed)
            21          --- new bullet roll speed (This will be zero for every bullet)
            22, 23, 24  --- new bullet acceleration in spheric cordinates (yaw, pitch, speed) (This will be zero for every bullet)
            25          --- new bullet roll acceleration(This wil be zero for every bullet)

            26          --- Killed by player id (if zero not killed)
            """

            if addr not in self.clients:
                if len(self.player_ids) == 0:
                    new_player_id = 1
                else:
                    new_player_id = self.player_ids[-1]+1

                self.player_ids.append(new_player_id)
                new_player = Player(addr, new_player_id)
                self.clients[addr] = new_player

            for client in self.clients.values():
                header = (self.clients[addr].id, client.id)
                packet = header+decoded_data

                if client != self.clients[addr]:
                    self.serverSocket.sendto(self.encode(packet), client.addr)


if __name__ == "__main__":
    s = Server()
    s.start()
