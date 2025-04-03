from engine.core.Game import Game
from engine.core.Camera import Camera
from engine.core.Utils import Utils
from engine.core_ext.Input import Input
from engine.core_ext.Maths import Maths

from mayhem.entities.Player import Player

import config

from pyglet.math import Vec2, Vec3, Mat3, Mat4, Quaternion
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
        mouse = Input.mouse

        movement_vertical = keys[config.KEY_BINDS.vertical[0]] - keys[config.KEY_BINDS.vertical[1]]
        movement_horizontal = keys[config.KEY_BINDS.horizontal[0]] - keys[config.KEY_BINDS.horizontal[1]]
        
        roll_direction = keys[config.KEY_BINDS.roll[1]] - keys[config.KEY_BINDS.roll[0]]

        movement = Vec3(movement_vertical, 0, movement_horizontal)
        
        self.acceleration = movement * config.thrust_force * delta
        self.rotation_acceleration = Vec3(0, 0, roll_direction * 8) * 60 * delta
        # self.rotation_acceleration = Vec3(pitch_direction, yaw_direction, roll_direction) * delta * 314
        

        if keys[config.KEY_BINDS.thrust]:
            forward = self.get_forward_vector()

            self.acceleration += forward * config.thrust_force * delta
    
    def update_camera_position(self, delta):
        forward = self.get_forward_vector()

        if forward.length == 0:
            return
        
        Camera.active_camera.pos = forward * -10 + self.pos + Vec3(4, 0, 0) # this does *NOT* work if the camera is rotated, uh oh
        Camera.active_camera.target = forward * 20 + self.pos