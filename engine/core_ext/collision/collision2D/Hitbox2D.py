"""
Contains the Hitbox2D class

authors: BAaboe
"""

from engine.core_ext.collision.collision2D.Hitarea2D import Hitarea2D

from pyglet.math import Vec2, Vec3


class Hitbox2D(Hitarea2D):
    """
    Subclass of Hitarea2D that gives info about a 2D box
    """

    def __init__(self, object_pos: Vec2, box_pos: Vec2, box_size: Vec2, box_rotation: float):
        """
        Creates a 2D hitbox

        Keyword arguments:
            object_pos: The center position to the object you want a hitbox for
            box_pos: The position relative to the object you want your hitbox.
            box_size: The size of the hitbox
            box_rotation: The rotationi of the box

        """
        self.object_pos = object_pos

        self.box_pos = box_pos
        self.box_size = box_size
        self.box_rotation = box_rotation

    def furthestPoint(self, d: Vec3):
        d = d.normalize()
        points = []

        x = self.object_pos.x+self.box_pos.x-self.box_size.x/2
        y = self.object_pos.y+self.box_pos.y-self.box_size.y/2
        pos = Vec2(x, y).rotate(self.box_rotation)
        points.append(Vec3(pos.x, pos.y))

        x = self.object_pos.x+self.box_pos.x+self.box_size.x/2
        y = self.object_pos.y+self.box_pos.y-self.box_size.y/2
        pos = Vec2(x, y).rotate(self.box_rotation)
        points.append(Vec3(pos.x, pos.y))

        x = self.object_pos.x+self.box_pos.x-self.box_size.x/2
        y = self.object_pos.y+self.box_pos.y+self.box_size.y/2
        pos = Vec2(x, y).rotate(self.box_rotation)
        points.append(Vec3(pos.x, pos.y))

        x = self.object_pos.x+self.box_pos.x+self.box_size.x/2
        y = self.object_pos.y+self.box_pos.y+self.box_size.y/2
        pos = Vec2(x, y).rotate(self.box_rotation)
        points.append(Vec3(pos.x, pos.y))

        biggest = points[0]
        for point in points:
            if point.dot(d) > biggest.dot(d):
                biggest = point

        return biggest

    def update(self, object_pos: Vec2, rotation: float):
        """
        Updates the position and rotation.

        Parameters:
            object_pos: The position of the object the hitarea is associated with
        """
        self.object_pos = object_pos
        self.box_rotation = rotation

    def center(self):
        center = self.object_pos + self.box_pos
        return Vec3(center.x, center.y,0)
