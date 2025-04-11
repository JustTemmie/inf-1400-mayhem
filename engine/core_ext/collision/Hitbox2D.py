from Hitarea import Hitarea

from pyglet.math import Vec2

from typing import Tuple


class Hitbox2D(Hitarea):
    def __init__(self, object_pos: Vec2, object_rot: float,
                 box_pos: Vec2, box_size: Vec2):
        """
        Creates a 2D hitbox

        Keyword arguments:
        object_pos -- the center position to the object you want a hitbox for
        object_rot -- the rotation in radians the object has
        box_pos    -- the position relative to the object you want your hitbox.
        box_size   -- the size of the hitbox

        """
        self.object_pos = object_pos
        self.object_rot = object_rot

        self.box_size = box_size
        self.box_pos = box_pos

        super.__init__("2dbox")

    def colliding_with(self, area: Hitarea):
        if area.type == "2dbox":
            my_x = self.object_pos.x + self.box_pos.x
            my_y = self.object_pos.y + self.box_pos.y
            my_w = self.box_size.x
            my_h = self.box_size.y

            coli_x = area.object_pos.x + area.box_pos.x
            coli_y = area.object_pos.y + area.box_pos.y
            coli_w = area.box_size.x
            coli_h = area.box_size.y

            if (coli_x-coli_w/2) < (my_x+my_w/2) & (my_x-my_w/2) < (coli_x+coli_w/2):
                if (coli_y-coli_h/2) < (my_y+my_h/2) & (my_y-my_h/2) < (coli_y+coli_h/2):
                    return False
        elif area.type == "2dsphere":
            # Sphere collision
            pass

        # Could also do with 3d objects

    def update_object(self, object_pos: Vec2, object_rot: float):
        self.object_pos = object_pos
        self.object_rot = object_rot
