from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core.Maths import Maths
from engine.core_ext.Entity3D import Entity3D

import config

from pyglet.math import Vec3

import pyglet
import typing
import logging


class Player(Entity3D):
    def user_init(self):
        print("new ship!")

    def process(self, delta):
        # print(f"frame tick!! {delta}")
        # self.roll += delta
        pass

    def engine_process(self, delta):
        logging.debug(f"player pos: {self.pos}")
        
        self.rotation_velocity = Vec3(1, 0.6, 0.3)

        # Purely experimental
        # self.velocity = Vec3(self.velocity.x + self.acceleration.x,
        #                     self.velocity.y + self.acceleration.y,
        #                     self.velocity.z + self.acceleration.z)
        # self.roll_velocity = self.roll_velocity + self.roll_acceleration
        # self.yaw = self.velocity.x
        # self.pitch = self.velocity.y
        # self.roll = self.roll_velocity
        
    def user_instantiate(self, game: Game):
        model_scene = pyglet.resource.scene(Utils.get_model_path("axes"))

        self.model = model_scene.create_models(batch=game.main_batch)[0]

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

