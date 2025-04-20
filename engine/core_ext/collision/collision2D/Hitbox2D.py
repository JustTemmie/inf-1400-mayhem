"""
2D Hitbox, can check for collisions with other 2D areas

authors: BAaboe
"""


from engine.core_ext.collision.collision2D.Hitarea2D import Hitarea2D

from pyglet.math import Vec2

from typing import Tuple

import math


class Hitbox2D(Hitarea2D):
    def __init__(self, object_pos: Vec2, area_pos: Vec2, box_size: Vec2):
        """
        Creates a 2D hitbox

        Keyword arguments:
        object_pos -- the center position to the object you want a hitbox for
        area_pos   -- the position relative to the object you want your hitbox.
        box_size   -- the size of the hitbox

        """
        self.object_pos = object_pos

        self.box_size = box_size
        self.area_pos = area_pos

        return super().__init__("2dbox")

    def colliding_with(self, area: Hitarea2D):
        my_x = self.object_pos.x + self.box_pos.x
        my_y = self.object_pos.y + self.box_pos.y
        my_w = self.box_size.x
        my_h = self.box_size.y

        coli_x = area.object_pos.x + area.area_pos.x
        coli_y = area.object_pos.y + area.area_pos.y
        if area.type == "2dbox":
            coli_w = area.box_size.x
            coli_h = area.box_size.y

            if (coli_x-coli_w/2) < (my_x+my_w/2) & (my_x-my_w/2) < (coli_x+coli_w/2):
                if (coli_y-coli_h/2) < (my_y+my_h/2) & (my_y-my_h/2) < (coli_y+coli_h/2):
                    return True
        elif area.type == "2dsphere":
            test_x = coli_x
            test_y = coli_y
            if my_x-my_w/2 > coli_x:
                test_x = my_x-my_w/2
            elif my_x+my_w/2 < coli_x:
                test_x = my_x+my_w/2
            if my_y-my_h/2 > coli_y:
                test_y = my_y-my_h/2
            elif my_y+my_h/2 < coli_y:
                test_y = my_y+my_h/2

            # Pythagoras
            distance = math.sqrt((coli_x-test_x)**2 + (coli_y-test_y)**2)

            if distance < area.sphere_radius:
                return True

        return False

        # Could also do with 3d objects. Maybe

    def update_object(self, object_pos: Vec2):
        self.object_pos = object_pos
