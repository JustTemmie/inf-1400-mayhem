"""
Contains the RemotePlayer class
Authors: BAaboe (i'll replace names at handin)
"""

from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from mayhem.entities.players.Player import Player
from mayhem.entities.Bullet import Bullet

import config

from pyglet.math import Vec3

import typing
import random
import pyglet

class RemotePlayer(Player):
    """
    Simple child class of the generic Player class.
    """

    def engine_process(self, delta):
        pass

        # Purely experimental
        # self.velocity = Vec3(self.velocity.x + self.acceleration.x,
        #                     self.velocity.y + self.acceleration.y,
        #                     self.velocity.z + self.acceleration.z)
        # self.roll_velocity = self.roll_velocity + self.roll_acceleration
        # self.yaw = self.velocity.x
        # self.pitch = self.velocity.y
        # self.roll = self.roll_velocity

    def user_init(self):
        self.hitboxes = [Hitsphere3D(self.pos, Vec3(0, 0, 0), 1)]

        super().user_init()
    
    def shoot(self, packet):
        bullet = Bullet()
        bullet.owner = packet.packet.from_id
        bullet.pos = packet.packet.player_pos
        bullet.rotation = packet.packet.player_rotation
        bullet.velocity = packet.packet.player_velocity + self.get_forward_vector() * config.BULLET_SPEED
        bullet.instantiate()

        if config.PLAY_SFX:
            source = pyglet.media.load(random.choice(self.laser_sfx), streaming=True)
            self.audio_player.position = self.pos
            self.audio_player.queue(source)
            self.audio_player.play()


    def update_pos(self, packet: typing.NamedTuple):
        """
        Updates the position, velocity and hitbox of the player.

        Parameters:
            packet: The network packet with the new position
        """
        self.pos = packet.packet.player_pos
        self.velocity = packet.packet.player_velocity
        self.acceleration = packet.packet.player_acceleration
        self.rotation = packet.packet.player_rotation
        self.rotation_velocity = packet.packet.player_rotation_velocity
        self.rotation_acceleration = packet.packet.player_rotation_acceleration

        for hitbox in self.hitboxes:
            hitbox.update(self.pos)

        # TODO: maybe do something when died?
        # Or maybe that is its own function
