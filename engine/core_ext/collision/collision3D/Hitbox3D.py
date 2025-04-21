"""
Contains the Hitbox3D class

authors: BAaboe
"""

from engine.core_ext.collision.collision3D.Hitarea3D import Hitarea3D

from pyglet.math import Vec3, Mat3

from math import cos, sin


class Hitbox3D(Hitarea3D):
    """
    Subclass of Hitarea3D that gives info about a 3D box
    """
    def __init__(self, object_pos: Vec3, object_rot: Vec3,
                 box_size: Vec3, box_pos: Vec3):
        """
        Creates a 3D hitbox

        Keyword arguments:
            object_pos: The center position to the object you want a hitbox for
            box_pos: the position relative to the object you want your hitbox.
            box_size: The size of the hitbox
            box_rotation: The rotation of the box

        """
        self.object_pos = object_pos
        self.object_rot = object_rot

        self.box_size = box_size
        self.box_pos = box_pos

    def furthestPoint(self, d: Vec3):
        theta = self.object_rot.x
        x_rot = Mat3(1, 0, 0,
                     0, cos(theta), -sin(theta),
                     0, sin(theta), cos(theta))

        theta = self.object_rot.y
        y_rot = Mat3(cos(theta), 0, sin(theta),
                     0, 1, 0,
                     -sin(theta), 0, cos(theta))

        theta = self.object_rot.z
        z_rot = Mat3(cos(theta), -sin(theta), 0,
                     sin(theta), cos(theta), 0,
                     0, 0, 1)

        d = d.normalize()

        points = []

        x = self.object_pos.x + self.box_pos.x-self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y-self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z-self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        x = self.object_pos.x + self.box_pos.x+self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y-self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z-self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        x = self.object_pos.x + self.box_pos.x-self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y+self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z-self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        x = self.object_pos.x + self.box_pos.x-self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y-self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z+self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        x = self.object_pos.x + self.box_pos.x+self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y+self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z-self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        x = self.object_pos.x + self.box_pos.x-self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y+self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z+self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        x = self.object_pos.x + self.box_pos.x+self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y-self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z+self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        x = self.object_pos.x + self.box_pos.x+self.box_size.x/2
        y = self.object_pos.y + self.box_pos.y+self.box_size.y/2
        z = self.object_pos.z + self.box_pos.z+self.box_size.z/2
        pos = Vec3(x, y, z)
        pos = x_rot @ y_rot @ z_rot @ pos
        points.append(pos)

        biggest = points[0]
        for point in points:
            if point.dot(d) > biggest.dot(d):
                biggest = point
        return biggest

    def update(self, object_pos: Vec3, object_rot: Vec3):
        """
        Updates the position and rotation.

        Parameters:
            object_pos: The position of the object the hitarea is associated with
        """
        self.object_pos = object_pos
        self.object_rot = object_rot

    def center(self):
        return self.object_pos+self.box_pos
