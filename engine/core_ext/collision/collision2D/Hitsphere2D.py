"""
2D Hitsphere, can check for collisions with other 2D areas

authors: BAaboe
"""


from engine.core_ext.collision.collision2D.Hitarea2D import Hitarea2D

from pyglet.math import Vec2, Vec3

import math


class Hitsphere2D(Hitarea2D):
    """
    Creates a 2D hitsphere

    Keyword arguments:
    object_pos      -- the center position to the object you want a hitbox for.
    sphere_pos      -- the position relative to the object you want your hitspher.
    sphere_radius   -- the radius the the hitspher.

    """

    def __init__(self, object_pos: Vec2, sphere_pos: Vec2, sphere_radius: float):
        self.object_pos = object_pos

        self.sphere_pos = sphere_pos
        self.sphere_radius = sphere_radius

    def furthestPoint(self, d: Vec3):
        d = d.normalize()

        pos = Vec3(self.object_pos.x + self.sphere_pos.x,
                   self.object_pos.y + self.sphere_pos.y, 0)

        return pos+d*self.sphere_radius

    def update(self, object_pos):
        self.object_pos = object_pos

    def center(self):
        center = self.object_pos+self.sphere_pos
        return Vec3(center.x, center.y)
