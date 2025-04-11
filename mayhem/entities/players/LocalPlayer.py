from engine.core.Game import Game
from engine.core.Camera import Camera
from engine.core.Utils import Utils
from engine.core.Window import Window
from engine.core_ext.Input import Input
from engine.core_ext.Maths import Maths

from mayhem.entities.players.Player import Player
from mayhem.entities.Bullet import Bullet

import config

from pyglet.math import Vec2, Vec3, Mat3, Mat4, Quaternion
from pyglet.window import key

import pyglet
import logging
import math
import time


class LocalPlayer(Player):
    def user_init(self):
        self.visible = False

        self.last_shoot_time = 0
        self.new_bullet = 0

        return super().user_init()

    def engine_process(self, delta):
        self.handle_input(delta)
        self.update_camera_position(delta)
        self.check_for_collision()

        logging.debug(f"player pos: {self.pos}")

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("test"))

        self.model = model_scene.create_models(batch=Player.game_object.main_batch)[0]

    def handle_input(self, delta):
        keys = Input.keyboard_keys
        standardized_mouse_position: Vec2 = (Input.mouse - Window.size / 2) / (Window.size / 2)  # generates a value between -1 and 1 for both axes
        logging.debug(f"mouse_pos: {standardized_mouse_position}")

        if ((abs(standardized_mouse_position.x) < config.mouse_virtual_joystick_deadzone
        and abs(standardized_mouse_position.y) < config.mouse_virtual_joystick_deadzone)
        or not config.mouse_movement):
            standardized_mouse_position = Vec2(0, 0)

        magnitude = max(1, standardized_mouse_position.length())
        normalized_mouse_position = standardized_mouse_position / magnitude

        key_movement_vertical = keys[config.KEY_BINDS.vertical[0]] - keys[config.KEY_BINDS.vertical[1]]
        key_movement_horizontal = keys[config.KEY_BINDS.horizontal[1]] - keys[config.KEY_BINDS.horizontal[0]]

        self.rotation_acceleration = Vec3(
            normalized_mouse_position.y + key_movement_vertical,
            normalized_mouse_position.x + key_movement_horizontal,
            0,
        ) * config.rotation_thrust_force * delta
        

        if keys[config.KEY_BINDS.thrust]:
            self.acceleration += self.get_forward_vector() * config.rear_thrust_force * delta

        if (keys[config.KEY_BINDS.shoot]
        and (time.time() - self.last_shoot_time) > config.SHOOTING_INTERVAL):
            self.shoot()
            self.last_shoot_time = time.time()


    def shoot(self):
        bullet = Bullet()
        bullet.owner = self.player_id
        bullet.pos = self.pos
        bullet.rotation = self.rotation
        bullet.velocity = self.get_forward_vector() * 30
        bullet.instantiate()

        self.new_bullet = 1

    def update_camera_position(self, delta):
        forward = self.get_forward_vector()

        if forward.length == 0:
            logging.warning("player does not have a valid forward vector, skipping camera positioning update")

        Camera.active_camera.pos = self.pos # this does *NOT* work if the camera is rotated, uh oh
        Camera.active_camera.target = self.pos + forward
        # Camera.active_camera.rotation = self.rotation
