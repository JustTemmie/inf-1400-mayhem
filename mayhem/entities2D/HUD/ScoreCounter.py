"""
Very simple entity that just draws the "deadzone" for the digital analogue stick.
Authors: JustTemmie (i'll replace names at handin)
"""

from engine.core.Window import Window
from engine.core.Entity2D import Entity2D
from mayhem.entities.players.LocalPlayer import LocalPlayer

import config

from pyglet.math import Vec3

import pyglet


class ScoreCounter(Entity2D):
    def user_instantiate(self):
        self.score_label = pyglet.text.Label(text="Score: 0", batch=self.game_object.UI_batch)
        self.score_label.weight = "bold"
        self.update_size_and_position()

    def prepare_draw(self, delta):
        self.score_label.text = f"Score: {LocalPlayer.instance.score}"
        self.update_size_and_position()

    def update_size_and_position(self):
        self.score_label.font_size = Window.size.y / 30
        self.score_label.position = Vec3(15, Window.size.y - 15 - self.score_label.font_size, 0)    