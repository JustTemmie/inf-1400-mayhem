from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core.Maths import Maths
from engine.core_ext.Entity3D import Entity3D

from mayhem.entities.Player import Player

from pyglet.math import Vec3

import pyglet

import typing

import config


class LocalPlayer(Player):
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
        super().engine_process(delta)

    def on_key_press(self, symbole, modifier):
        return
        # Purely experimental
        if symbole == config.KEY_BINDS["yaw"][0]:
            print("Yaw +")
            self.acceleration = Vec3(self.acceleration.x + Maths.radian_degree,
                                    self.acceleration.y,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["yaw"][1]:
            print("Yaw -")
            self.acceleration = Vec3(self.acceleration.x - Maths.radian_degree,
                                    self.acceleration.y,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][0]:
            print("Pitch +")
            self.acceleration = Vec3(self.acceleration.x,
                                    self.acceleration.y + Maths.radian_degree,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][1]:
            print("Pitch -")
            self.acceleration = Vec3(self.acceleration.x,
                                    self.acceleration.y - Maths.radian_degree,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["roll"][0]:
            print("Roll +")
            self.roll_acceleration += Maths.radian_degree
        if symbole == config.KEY_BINDS["roll"][1]:
            print("Roll -")
            self.roll_acceleration -= Maths.radian_degree
        if symbole == config.KEY_BINDS["shoot"]:
            print("Shoot")

    def on_key_release(self, symbole, modifier):
        return
        # Purely experimental
        if symbole == config.KEY_BINDS["yaw"][0]:
            print("Yaw +")
            self.acceleration = Vec3(self.acceleration.x - Maths.radian_degree,
                                    self.acceleration.y,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["yaw"][1]:
            print("Yaw -")
            self.acceleration = Vec3(self.acceleration.x + Maths.radian_degree,
                                    self.acceleration.y,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][0]:
            print("Pitch +")
            self.acceleration = Vec3(self.acceleration.x,
                                    self.acceleration.y - Maths.radian_degree,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][1]:
            print("Pitch -")
            self.acceleration = Vec3(self.acceleration.x,
                                    self.acceleration.y + Maths.radian_degree,
                                    self.acceleration.z)
        if symbole == config.KEY_BINDS["roll"][0]:
            print("Roll +")
            self.roll_acceleration -= Maths.radian_degree
        if symbole == config.KEY_BINDS["roll"][1]:
            print("Roll -")
            self.roll_acceleration += Maths.radian_degree
        if symbole == config.KEY_BINDS["shoot"]:
            print("Shoot stop")
