# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys

    sys.path.append(".")

from engine.core.Game import Game
from engine.core.Entity import Entity
from engine.core_ext.Netwoking import Networking

from mayhem.entities.players.Player import Player
from mayhem.entities.ExampleObject import ExampleObject

from mayhem.Packet import Packet

from mayhem.entities.players.LocalPlayer import LocalPlayer
from mayhem.entities.players.RemotePlayer import RemotePlayer
from mayhem.entities2D.HUD.movement_reticle import MovementReticle
from mayhem.entities.Bullet import Bullet

from pyglet.math import Vec3

import typing

import pyglet
import pyglet.window.key
import config


class Mayhem(Game):
    def init(self):
        self.player = LocalPlayer()
        self.player.pos = pyglet.math.Vec3(5, 0, 0)
        self.player.instantiate()

        self.spawn_test_objects()
        self.spawn_hud()

        self.networking = Networking(
            config.SERVER_PORT, config.SERVER_TEST_ADDRESS
        )  # FIXME: Should be changed later. Port and address should be a user input
        if self.networking.connected:
            self.networking.start_listen()  # Creates a thread that listens to the server.
            self.networking.send(Packet.player_to_packet(self.player))

        self.other_players: typing.Dict[int, RemotePlayer] = {}

    def spawn_hud(self):
        movement_reticle = MovementReticle()
        movement_reticle.instantiate()

    def spawn_test_objects(self):
        player = Player()
        player.pos = Vec3(-5, 0, 0)
        player.instantiate()

        player = Player()
        player.pos = Vec3(-5, 0, 15)
        player.instantiate()

        ExampleObject().instantiate()

        for i in range(100):
            object = ExampleObject()
            object.pos = Vec3(0, 0, i - 50)
            object.instantiate()

    def user_engine_process(self, delta):

        self._handle_network_input()
        self._send_update()
        pass

    def _send_update(self):
        if self.networking.connected:
            bullet = self.player.newest_bullet
            if not bullet:
                self.networking.send(Packet.player_to_packet(self.player))
            else:
                self.networking.send(Packet.player_to_packet(self.player, bullet))
                self.player.newest_bullet = None

    def _handle_network_input(self):
        self.networking.lock.acquire()  # Locks the queue so that two threads can not use it at the same time
        while not self.networking.q.empty():
            data = self.networking.q.get()
            packet = Packet.decode(data)
            if self.player.id == 0:
                self.player.id = packet.packet.to_id
            if packet.packet.from_id not in self.other_players:
                self.other_players[packet.packet.from_id] = RemotePlayer()
                self.other_players[packet.packet.from_id].instantiate()

            self.other_players[packet.packet.from_id].update_pos(packet)

            if packet.packet.bullet_pos != Vec3(0, 0, 0):
                b = Bullet()
                b.pos = packet.packet.bullet_pos
                b.velocity = packet.packet.bullet_velocity
                b.acceleration = packet.packet.bullet_acceleration
                b.rotation = packet.packet.bullet_rotation
                b.rotation_velocity = packet.packet.bullet_rotation_velocity
                b.rotation_acceleration = packet.packet.bullet_rotation_acceleration
                b.instantiate()

        self.networking.lock.release()
