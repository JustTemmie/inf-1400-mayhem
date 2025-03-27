from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core_ext.Maths import Maths
from engine.core.Entity3D import Entity3D

import config

from pyglet.math import Vec3

import pyglet
import typing
import logging


class Player(Entity3D):
    def user_init(self):
        print("new ship!")
        self.id = 0
        
        self.mass = 200 # kg

    def process(self, delta):
        # print(f"frame tick!! {delta}")
        # self.roll += delta
        pass

    def engine_process(self, delta):
        logging.debug(f"player pos: {self.pos}")
        
        self.rotation_velocity = Vec3(1, 0.6, 0.3)

    def user_instantiate(self, game: Game):
        model_scene = pyglet.resource.scene(Utils.get_model_path("axes"))

        self.model = model_scene.create_models(batch=game.main_batch)[0]