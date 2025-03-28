# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

from engine.core.Game import Game
from engine.core.Entity import Entity
from engine.core_ext.Netwoking import Networking

from mayhem.entities.Player import Player
from mayhem.entities.ExampleObject import ExampleObject

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
        self.player.pos = pyglet.math.Vec3(5, 0, 0)
        self.player.instantiate(self)

        #self.spawn_test_objects()

        self.networking = Networking(config.SERVER_PORT, config.SERVER_TEST_ADDRESS) # FIXME: Should be changed later. Port and address should be a user input
        if self.networking.connected:
            self.networking.start_listen()  # Creates a thread that listens to the server.
            self.networking.send(Packet.player_to_packet(self.player))

        self.other_players: typing.Dict[int, RemotePlayer] = {}

    def spawn_test_objects(self):
        player = Player()
        player.pos = pyglet.math.Vec3(-5, 0, 0)
        player.instantiate(self)

        player = Player()
        player.pos = pyglet.math.Vec3(-5, 0, 15)
        player.instantiate(self)

        ExampleObject().instantiate(self)

    def user_engine_process(self, delta):

        self._handle_network_input()
        self._send_update()
        pass

    def _send_update(self):
        if self.networking.connected:
            self.networking.send(Packet.player_to_packet(self.player))

    def _handle_network_input(self):
        self.networking.lock.acquire()  # Locks the queue so that two threads do not use it at the same time
        while not self.networking.q.empty():
            data = self.networking.q.get()
            packet = Packet.decode(data)
            if self.player.id == 0:
                self.player.id = packet.packet.to_id
            if packet.packet.from_id not in self.other_players:
                self.other_players[packet.packet.from_id] = RemotePlayer()
                self.other_players[packet.packet.from_id].instantiate(self)

            self.other_players[packet.packet.from_id].update_pos(packet)

        self.networking.lock.release()
