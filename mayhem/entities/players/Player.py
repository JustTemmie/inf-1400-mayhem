"""
Contains the Player class
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Entity3D import Entity3D
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D
from engine.extras.Utils import Utils

import config

from pyglet.math import Vec3

import pyglet


class Player(Entity3D):
    """
    Generic Player class. 
    """

    laser_sfx = [
        "assets/sfx/lasers/laser_1_mono.ogg",
        "assets/sfx/lasers/laser_2_mono.ogg",
        "assets/sfx/lasers/laser_3_mono.ogg",
        "assets/sfx/lasers/laser_4_mono.ogg",
        "assets/sfx/lasers/laser_5_mono.ogg",
        "assets/sfx/lasers/laser_6_mono.ogg",
    ]
    
    def user_init(self):
        self.player_id = 0

        self.mass = 2_000  # kg
        self.area = 1  # m^2, affects the objects interaction with air
        self.drag_coeficient = 1.225
        self.ignore_friction: bool = False

        self.hitboxes = [Hitsphere3D(self.pos, Vec3(0, 0, 0), 2.5)]

        if config.PLAY_SFX:
            self.audio_player = pyglet.media.Player()
            self.audio_player.min_distance = 35
            self.audio_player.max_distance = 350

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("ship"))

        self.model = model_scene.create_models(batch=Entity3D.game_object.main_batch)[0]
