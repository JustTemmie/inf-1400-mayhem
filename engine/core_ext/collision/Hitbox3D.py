from Hitarea import Hitarea

from pyglet.math import Vec3

from typing import Tuple


class Hitbox3D(Hitarea):
    def __init__(self, object_pos: Vec3, object_rot: Vec3,
                 box_size: Vec3, box_pos: Vec3):
        self.object_pos = object_pos
        self.object_rot = object_rot

        self.box_size = box_size
        self.box_pos = box_pos

        super.__init__("2dbox")

    def colliding_with(area: Hitarea):
        if area.type == "2dbox":
            # Box collision
            pass
        elif area.type == "2dsphere":
            # Sphere collision
            pass

    def update_object(self, object_pos: Vec3, object_rot: Vec3):
        self.object_pos = object_pos
        self.object_rot = object_rot
