"""
( write more later )
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core.Entity3D import Entity3D

import config

from pyglet.math import Vec3

import pyglet
import typing
import logging


class Player(Entity3D):
    def user_init(self):
        logging.info("new ship!")
        self.player_id = 0

        self.mass = 200  # kg
        self.area = 1  # m^2, affects the objects interaction with air
        self.drag_coeficient = 1.225
        self.ignore_friction: bool = False

    def process(self, delta):
        # self.roll += delta
        pass

    def engine_process(self, delta):
        self.rotation_velocity = Vec3(1, 0.6, 0.3)

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("axes"))

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]
