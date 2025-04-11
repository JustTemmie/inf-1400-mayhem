"""
Very simple entity that just draws the "deadzone" for the digital analogue stick.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Entity2D import Entity2D

import config


import pyglet


class MovementReticle(Entity2D):
    def user_instantiate(self):
        if config.mouse_movement:
            radius = Window.size.y * config.mouse_virtual_joystick_deadzone / 2

            self.middle_circle = pyglet.shapes.Circle(
                x=Window.size.x / 2 - radius * 1.5,
                y=Window.size.y / 2 - radius * 1.5,
                radius=radius,
                color=(255, 80, 80, 55),
                batch=self.render_batch,
            )