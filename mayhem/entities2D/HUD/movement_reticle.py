from engine.core.Game import Game
from engine.core.Window import Window
from engine.core.Entity2D import Entity2D
from engine.core.Utils import Utils

import config

from pyglet.math import Vec3

import pyglet
import typing
import logging


class MovementReticle(Entity2D):
    # def user_init(self):
    #     self.id = 0

    def user_instantiate(self):
        if config.mouse_movement:
            radius = Window.size.y * config.virtual_joystick_deadzone / 2

            self.middle_circle = pyglet.shapes.Circle(
                x=Window.size.x / 2 - radius * 2,
                y=Window.size.y / 2 - radius * 2,
                radius=radius,
                color=(255, 80, 80, 55),
                batch=self.render_batch,
            )

    def prepare_draw(self, delta):
        pass
        # self.middle_circle.draw()
