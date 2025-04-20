"""
2D Hitsphere, can check for collisions with other 2D areas

authors: BAaboe
"""


from engine.core_ext.collision.collision2D.Hitarea2D import Hitarea2D

from pyglet.math import Vec2

import math


class Hitsphere2D(Hitarea2D):
    def __init__(self, object_pos: Vec2, area_pos: Vec2, sphere_radius: float):
        """
        Creates a 2D hitbox

        Keyword arguments:
        object_pos      -- the center position to the object you want a hitbox for
        area_pos        -- the position relative to the object you want your hitspher.
        sphere_radius   -- the radius the the hitspher.

        """
        self.object_pos = object_pos

        self.area_pos = area_pos
        self.sphere_radius = sphere_radius

        super().__init__("2dsphere")

    def colliding_with(self, area: Hitarea2D):
        my_x = self.object_pos.x+self.sphere_pos.x
        my_y = self.object_pos.y+self.sphere_pos.y

        coli_x = area.object_pos.x+area.area_pos.x
        coli_y = area.object_pos.y+area.area_pos.y
        if area.type == "2dbox":
            coli_w = area.box_size.x
            coli_h = area.box_size.y

            test_x = my_x
            test_y = my_y

            if coli_x-coli_w/2 < my_x:
                test_x = coli_x-coli_w/2
            elif coli_x+coli_w/2 > my_x:
                test_x = coli_x+coli_w/2
            if coli_y-coli_h/2 < my_x:
                test_y = coli_y-coli_h/2
            elif coli_y+coli_h/2 > my_x:
                test_y = coli_y+coli_h/2

            # Pythagoras
            distance = math.sqrt((my_x-test_x)**2 + (my_y-test_y)**2)

            if distance < self.sphere_radius:
                return False

        elif area.type == "2dsphere":
            # Phytagoras
            distance = math.sqrt((my_x-coli_x)**2 + (my_x-coli_x)**2)

            if distance < self.sphere_radius + area.sphere_radius:
                return True

        return False
