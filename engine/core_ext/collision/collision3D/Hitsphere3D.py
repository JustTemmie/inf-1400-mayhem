"""
Contains the Hitsphere3D class

authors: BAboe
"""

from engine.core_ext.collision.collision3D.Hitarea3D import Hitarea3D

from pyglet.math import Vec3


class Hitsphere3D(Hitarea3D):
    """
    Subclass of Hitarea3D that contains info about a 3D sphere
    """
    def __init__(self, object_pos: Vec3, sphere_pos: Vec3, sphere_radius: float):
        """
        Creates a 3D hitsphere

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

        return self.object_pos+self.sphere_pos+d*self.sphere_radius

    def update(self, object_pos):
        self.object_pos = object_pos

    def center(self):
        return self.object_pos + self.sphere_pos
