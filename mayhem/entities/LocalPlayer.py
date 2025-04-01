from engine.core.Game import Game
from engine.core.Camera import Camera
from engine.core.Utils import Utils
from engine.core_ext.Input import Input
from engine.core_ext.Maths import Maths

from mayhem.entities.Player import Player

import config

from pyglet.math import Vec2, Vec3, Mat3, Mat4
from pyglet.window import key

import pyglet
import logging
import math


class LocalPlayer(Player):
    def engine_process(self, delta):
        self.handle_input(delta)
        self.update_camera_position(delta)

        logging.debug(f"player pos: {self.pos}")
    
    def user_instantiate(self, game: Game):
        model_scene = pyglet.resource.scene(Utils.get_model_path("test"))

        self.model = model_scene.create_models(batch=game.main_batch)[0]

    def handle_input(self, delta):
        keys = Input.keyboard_keys

        pitch_direction = keys[config.KEY_BINDS.pitch[0]] - keys[config.KEY_BINDS.pitch[1]]
        yaw_direction = keys[config.KEY_BINDS.yaw[1]] - keys[config.KEY_BINDS.yaw[0]] # reverse?
        roll_direction = keys[config.KEY_BINDS.roll[1]] - keys[config.KEY_BINDS.roll[0]] # reverse?

        self.rotation_acceleration = Vec3(pitch_direction, yaw_direction, roll_direction) * delta * 314

        if keys[config.KEY_BINDS.thrust]:
            forward = self.get_forward_vector()

            self.acceleration += forward * config.thrust_force * delta
    
    def update_camera_position(self, delta):
        forward = self.get_forward_vector()

        if forward.length == 0:
            return
        
        Camera.active_camera.pos = forward * -10 + self.pos
        Camera.active_camera.target = forward * 50 + self.pos