"""
Contains Hitsphere2D class

authors: BAaboe
"""

from engine.core_ext.collision.collision2D.Hitarea2D import Hitarea2D

from pyglet.math import Vec2, Vec3


class Hitsphere2D(Hitarea2D):
    """
    Subclass of Hitarea2D that contains info about a 2D sphere
    """

    def __init__(self, object_pos: Vec2, sphere_pos: Vec2, sphere_radius: float):
        """
        Creates a 2D hitsphere

        Keyword arguments:
            object_pos: The center position to the object you want a hitbox for.
            sphere_pos: The position relative to the object you want your hitspher.
            sphere_radius: The radius the the hitspher.

        """
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
