"""
( write more later )
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Game import Game
from engine.core_ext.Netwoking import Networking
import engine.extras.logger # this is just to init the module, do not remove even though it's unused

from mayhem.entities.players.Player import Player
from mayhem.entities.ExampleObject import ExampleObject

from mayhem.Packet import Packet

from mayhem.entities.players.LocalPlayer import LocalPlayer
from mayhem.entities.players.RemotePlayer import RemotePlayer
from mayhem.entities.Bullet import Bullet

from mayhem.entities2D.HUD.MovementReticle import MovementReticle
from mayhem.entities2D.HUD.ScoreCounter import ScoreCounter

from pyglet.math import Vec3

import typing

import pyglet
import config


class Mayhem(Game):
    def init(self):
        self.player = LocalPlayer()
        self.player.pos = pyglet.math.Vec3(2, -10, 0)
        self.player.instantiate()

        # self.spawn_test_objects()
        self.spawn_hud()

        self.networking = Networking(
            config.SERVER_PORT, config.SERVER_TEST_ADDRESS
        )  # FIXME: Should be changed later. Port and address should be a user input
        if self.networking.connected:
            self.networking.start_listen()  # Creates a thread that listens to the server.
            self.networking.send(Packet.player_to_packet(self.player))

        self.other_players: typing.Dict[int, RemotePlayer] = {}

    def spawn_hud(self):
        MovementReticle().instantiate()
        ScoreCounter().instantiate()
        

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
            self.networking.send(Packet.player_to_packet(self.player, self.player.new_bullet))
            self.player.new_bullet = 0

    def _handle_network_input(self):
        self.networking.lock.acquire()  # Locks the queue so that two threads can not use it at the same time
        while not self.networking.q.empty():
            data = self.networking.q.get()
            packet = Packet.decode(data)
            if self.player.player_id == 0:
                self.player.player_id = packet.packet.to_id
            if packet.packet.from_id not in self.other_players:
                self.other_players[packet.packet.from_id] = RemotePlayer()
                self.other_players[packet.packet.from_id].instantiate()

            self.other_players[packet.packet.from_id].update_pos(packet)

            if packet.packet.new_bullet:
                b = Bullet()
                b.owner = packet.packet.from_id
                b.pos = packet.packet.player_pos
                b.velocity = packet.packet.player_rotation
                b.velocity = self.other_players[packet.packet.from_id].get_forward_vector()*config.BULLET_SPEED
                b.instantiate()

        self.networking.lock.release()
