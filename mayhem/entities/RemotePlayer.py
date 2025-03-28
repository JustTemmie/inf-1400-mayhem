from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core_ext.Maths import Maths
from engine.core.Entity3D import Entity3D

from mayhem.entities.Player import Player

from pyglet.math import Vec3

import pyglet

import typing

import config


class RemotePlayer(Player):
    def engine_process(self, delta):
        print(f"engine tick!! {delta}")

        # Purely experimental
        # self.velocity = Vec3(self.velocity.x + self.acceleration.x,
        #                     self.velocity.y + self.acceleration.y,
        #                     self.velocity.z + self.acceleration.z)
        # self.roll_velocity = self.roll_velocity + self.roll_acceleration
        # self.yaw = self.velocity.x
        # self.pitch = self.velocity.y
        # self.roll = self.roll_velocity

    def update_pos(self, packet: typing.NamedTuple):
        self.pos = packet.packet.player_pos
        self.velocity = packet.packet.player_velocity
        self.acceleration = packet.packet.player_acceleration
        self.rotation = packet.packet.player_rotation
        self.rotation_velocity = packet.packet.player_rotation_velocity
        self.rotation_acceleration = packet.packet.player_rotation_acceleration

        # TODO: maybe do something when died?
        # Or maybe that is its own function
