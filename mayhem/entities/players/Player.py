"""
Contains the Player class
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.extras.Utils import Utils
from engine.core.Entity3D import Entity3D

import pyglet


class Player(Entity3D):
    """
    Generic Player class. 
    """

    def user_init(self):
        self.player_id = 0

        self.mass = 2_000  # kg
        self.area = 1  # m^2, affects the objects interaction with air
        self.drag_coeficient = 1.225
        self.ignore_friction: bool = False

        self.audio_player = pyglet.media.Player()

    def process(self, delta):
        self.audio_player.position = self.pos

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("ship"))

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]
