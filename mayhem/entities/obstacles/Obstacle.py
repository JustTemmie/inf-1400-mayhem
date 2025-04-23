"""
Generic obstacle class for interactions with the player
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Utils import Utils
from engine.core.Entity3D import Entity3D
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from mayhem.entities.Bullet import Bullet

from pyglet.math import Vec3

import pyglet


class Obstacle(Entity3D):
    def engine_process(self, delta):
        self.check_for_collision(delta)
    
    def handle_collision(self, entity: Entity3D, delta):
        if entity.__class__ == Bullet:
            entity.free()