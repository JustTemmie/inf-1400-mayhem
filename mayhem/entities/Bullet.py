"""
Contains the bullet class
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Entity3D import Entity3D
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D

import pyglet
from pyglet.math import Vec3


class Bullet(Entity3D):
    """
    Bullet class contains info about a bullet
    """

    bullet_colours = ["blue", "green", "grey", "purple", "red", "yellow"]

    def user_init(self):
        self.mass = 0.01
        self.ignore_friction = True

        self.owner = 0
        self.age = 0

        self.log_spawn = False

    def user_instantiate(self):
        # decide colour based on owner ID such that colours are synced between players
        colour = Bullet.bullet_colours[self.owner % len(Bullet.bullet_colours)]

        model_scene = pyglet.resource.scene(f"assets/models/bullets/{colour}/bullet.obj")

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]

        self.hitboxes = [Hitsphere3D(self.pos, Vec3(0, 0, 0), 1)]

    def engine_process(self, delta):
        self.age += delta

        if self.age > 10:
            self.free()
            Entity3D.game_object.main_batch.invalidate()

        for hitbox in self.hitboxes:
            hitbox.update(self.pos)
