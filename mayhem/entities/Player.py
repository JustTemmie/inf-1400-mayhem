from engine.core.Game import Game
from engine.core_ext.Entity3D import Entity3D

from pyglet.math import Vec3

import pyglet

import typing

import config

class Player(Entity3D):
    def user_init(self):
        print("new ship!")

    def process(self, delta):
        #print(f"frame tick!! {delta}")
        self.draw()

    def engine_process(self, delta):
        #print(f"engine tick!! {delta}")

        # Purely experimental
        self.velocity= Vec3(self.velocity.x + self.acceleration.x,
                            self.velocity.y + self.acceleration.y,
                            self.velocity.z + self.acceleration.z)
        self.roll_velocity = self.roll_velocity + self.roll_acceleration
        self.yaw = self.velocity.x
        self.pitch = self.velocity.y
        self.roll = self.roll_velocity

    def user_instantiate(self, game: Game):
        model_scene = pyglet.resource.scene("assets/models/axes.obj")

        self.model = model_scene.create_models(batch=game.main_batch)[0]

    def on_key_press(self, symbole, modifier):
        # Purely experimental
        if symbole == config.KEY_BINDS["yaw"][0]:
            print("Yaw +")
            self.acceleration = Vec3(self.acceleration.x + 0.0174532925,
                                     self.acceleration.y,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["yaw"][1]:
            print("Yaw -")
            self.acceleration = Vec3(self.acceleration.x - 0.0174532925,
                                     self.acceleration.y,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][0]:
            print("Pitch +")
            self.acceleration = Vec3(self.acceleration.x,
                                     self.acceleration.y + 0.0174532925,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][1]:
            print("Pitch -")
            self.acceleration = Vec3(self.acceleration.x,
                                     self.acceleration.y - 0.0174532925,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["roll"][0]:
            print("Roll +")
            self.roll_acceleration += 0.0174532925
        if symbole == config.KEY_BINDS["roll"][1]:
            print("Roll -")
            self.roll_acceleration -= 0.0174532925
        if symbole == config.KEY_BINDS["shoot"]:
            print("Shoot")

    def on_key_release(self, symbole, modifier):
        # Purely experimental
        if symbole == config.KEY_BINDS["yaw"][0]:
            print("Yaw +")
            self.acceleration = Vec3(self.acceleration.x - 0.0174532925,
                                     self.acceleration.y,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["yaw"][1]:
            print("Yaw -")
            self.acceleration = Vec3(self.acceleration.x + 0.0174532925,
                                     self.acceleration.y,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][0]:
            print("Pitch +")
            self.acceleration = Vec3(self.acceleration.x,
                                     self.acceleration.y - 0.0174532925,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["pitch"][1]:
            print("Pitch -")
            self.acceleration = Vec3(self.acceleration.x,
                                     self.acceleration.y + 0.0174532925,
                                     self.acceleration.z)
        if symbole == config.KEY_BINDS["roll"][0]:
            print("Roll +")
            self.roll_acceleration -= 0.0174532925
        if symbole == config.KEY_BINDS["roll"][1]:
            print("Roll -")
            self.roll_acceleration += 0.0174532925
        if symbole == config.KEY_BINDS["shoot"]:
            print("Shoot stop")

