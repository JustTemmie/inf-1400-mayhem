from engine.core.Game import Game
from engine.core.Utils import Utils
from engine.core_ext.Input import Input
from engine.core_ext.Maths import Maths
from engine.core.Entity3D import Entity3D

from mayhem.entities.Player import Player

from pyglet.math import Vec2, Vec3
from pyglet.window import key

import pyglet
import typing
import config


class LocalPlayer(Player):
    def engine_process(self, delta):
        self.handle_input(delta)
        super().engine_process(delta)

    def handle_input(self, delta):
        keys = Input.keyboard_keys
        
        input_vector = Vec2(
            keys[key.A] - keys[key.D],
            keys[key.W] - keys[key.S]
        )
        
        self.acceleration = Vec3(input_vector.x, input_vector.y, 0)