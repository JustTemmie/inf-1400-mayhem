"""
Very simple entity that just displays the player's health in the top left of the screen.
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Entity2D import Entity2D
from mayhem.entities.players.LocalPlayer import LocalPlayer

from pyglet.math import Vec3

import pyglet
import math


class FuelCounter(Entity2D):
    def user_instantiate(self):
        self.score_label = pyglet.text.Label(text="Fuel: 0", batch=self.game_object.UI_batch)
        self.update_size_and_position()

    def prepare_draw(self, delta):
        self.score_label.text = f"Fuel: {int(math.ceil(LocalPlayer.instance.fuel))}"
        self.update_size_and_position()

    def update_size_and_position(self):
        self.score_label.font_size = Window.size.y / 30
        self.score_label.position = Vec3(15, Window.size.y - 95 - self.score_label.font_size, 0)
