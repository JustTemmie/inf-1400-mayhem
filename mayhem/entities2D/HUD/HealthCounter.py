"""
Very simple entity that just displays the player's health in the top left of the screen.
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Entity2D import Entity2D
from engine.core_ext.Colour import Colour
from mayhem.entities.players.LocalPlayer import LocalPlayer

from pyglet.math import Vec3

import pyglet
import config


class HealthCounter(Entity2D):
    def user_instantiate(self):
        width = Window.size.x*config.MAX_UI_BAR_WIDTH
        height = width*config.UI_BAR_HEIGHT

        margin = height*config.UI_BAR_MARGIN

        x = 15
        y = Window.size.y - Window.size.y/30 - height*2

        self.health_bar_bc = pyglet.shapes.Rectangle(x = x, y = y,
                                                     width = width, height = height,
                                                     color = Colour.GREY,
                                                     batch = self.game_object.UI_batch)

        margin = config.UI_BAR_MARGIN
        self.health_bar = pyglet.shapes.Rectangle(x = x+margin, y = y+margin,
                                                  width = width-margin*2, height = height-margin*2,
                                                  color = Colour.RED,
                                                  batch = self.game_object.UI_batch)

    def prepare_draw(self, delta):
        width = Window.size.y*config.MAX_UI_BAR_WIDTH
        height = width*config.UI_BAR_HEIGHT

        margin = height*config.UI_BAR_MARGIN

        x = 15
        y = Window.size.y - Window.size.y/30 - height*2

        self.health_bar_bc.y = y
        self.health_bar_bc.width = width
        self.health_bar_bc.height = height

        self.health_bar.x = x+margin
        self.health_bar.y = y+margin
        self.health_bar.width = (width-margin*2)*LocalPlayer.instance.health/100
        self.health_bar.height = height-margin*2
