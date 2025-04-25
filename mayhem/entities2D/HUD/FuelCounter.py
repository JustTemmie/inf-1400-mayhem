"""
Contains the FuelCounter class
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Entity2D import Entity2D
from engine.core_ext.Colour import Colour
from mayhem.entities.players.LocalPlayer import LocalPlayer

import pyglet
import config

class FuelCounter(Entity2D):
    """
    Very simple entity that just displays the player's Fuel in the top left of the screen.
    """
    def user_instantiate(self):
        width = Window.size.x*config.MAX_UI_BAR_WIDTH
        height = width*config.UI_BAR_HEIGHT

        margin = height*config.UI_BAR_MARGIN

        x = 15
        y = Window.size.y - Window.size.y/30 - height*3.5

        self.fuel_bar_bc = pyglet.shapes.Rectangle(x = x, y = y,
                                                     width = width, height = height,
                                                     color = Colour.GREY,
                                                     batch = self.game_object.UI_batch)

        self.fuel_bar = pyglet.shapes.Rectangle(x = x+margin, y = y+margin,
                                                  width = width-margin*2, height = height-margin*2,
                                                  color = Colour.YELLOW,
                                                  batch = self.game_object.UI_batch)

    def prepare_draw(self, delta):
        width = Window.size.y*config.MAX_UI_BAR_WIDTH
        height = width*config.UI_BAR_HEIGHT

        margin = height*config.UI_BAR_MARGIN

        x = 15
        y = Window.size.y - Window.size.y/30 - height*3.5

        self.fuel_bar_bc.y = y
        self.fuel_bar_bc.width = width
        self.fuel_bar_bc.height = height

        self.fuel_bar.x = x+margin
        self.fuel_bar.y = y+margin
        self.fuel_bar.width = (width-margin*2)*LocalPlayer.instance.fuel / config.MAX_FUEL
        self.fuel_bar.height = height-margin*2
