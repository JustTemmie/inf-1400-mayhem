# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

from engine.core.Game import Game
from engine.core_ext.Entity import Entity
from engine.core_ext.Netwoking import Networking

from mayhem.entities.Player import Player

from mayhem.Packet import Packet

from mayhem.entities.LocalPlayer import LocalPlayer
from mayhem.entities.RemotePlayer import RemotePlayer

import typing

import pyglet
import pyglet.window.key
import config

class Mayhem(Game):
    def init(self):
        self.player = LocalPlayer()
        self.player.instantiate(self)
        self.game_window.event("on_key_press")(self.player.on_key_press)
        self.game_window.event("on_key_release")(self.player.on_key_release)

        self.networking = Networking(config.SERVER_PORT, config.SERVER_TEST_ADDRESS) # FIXME: Should be changed later. Port and address should be a user input
        if self.networking.connected:
            self.networking.start_listen()  # Creates a thread that listens to the server.
            self.networking.send(Packet()) # FIXME: Remove

        self.other_players: typing.Dict[int, RemotePlayer] = {}

    def user_engine_process(self, delta):

        self._handle_network_input()
        pass

    def _handle_network_input(self):
        self.networking.lock.acquire()  # Locks the queue so that two threads do not use it at the same time
        while not self.networking.q.empty():
            data = self.networking.q.get()
            packet = Packet.decode(data)

        self.networking.lock.release()


