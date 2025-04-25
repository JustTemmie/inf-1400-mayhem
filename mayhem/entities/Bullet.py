"""
Contains the bullet class
Authors: BAaboe (i'll replace names at handin)
"""

from engine.core.Entity3D import Entity3D
from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core_ext.collision.collision3D.Hitbox3D import Hitbox3D
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D

import pyglet
from pyglet.math import Vec3
import gc
import time


class Bullet(Entity3D):
    """
    Bullet class contains info about a bullet
    """
    def user_init(self):
        self.mass = 0.01
        self.ignore_friction = True

        self.owner = 0
        self.age = 0

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("rocket"))

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]

        self.hitboxes = [Hitsphere3D(self.pos, Vec3(0, 0, 0), 1)]

    def engine_process(self, delta):
        self.age += delta

        if self.age > 10:
            self.free()
            Entity3D.game_object.main_batch.invalidate()

        for hitbox in self.hitboxes:
            hitbox.update(self.pos)
