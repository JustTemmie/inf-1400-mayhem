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
        self.last_shoot_time = 0

        self.newest_bullet: Bullet = None
        return super().user_init()

    def engine_process(self, delta):
        self.handle_input(delta)
        self.update_camera_position(delta)
        self.check_for_collision()

        logging.debug(f"player pos: {self.pos}")
        print(f"player pos: {self.pos}")

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("test"))

        self.model = model_scene.create_models(batch=Player.game_object.main_batch)[0]

    def handle_input(self, delta):
        self.handle_keys(delta)
        # self.handle_mouse(delta)

        # self.rotation_acceleration = Vec3(0, 0, roll_direction * 8) * config.roll_thrust_force * delta
        # self.rotation_acceleration = Vec3(pitch_direction, yaw_direction, roll_direction) * delta * 314

    def handle_keys(self, delta):
        keys = Input.keyboard_keys

        movement_vertical = (
            keys[config.KEY_BINDS.vertical[0]] - keys[config.KEY_BINDS.vertical[1]]
        )
        movement_horizontal = (
            keys[config.KEY_BINDS.horizontal[0]] - keys[config.KEY_BINDS.horizontal[1]]
        )

        pitch_direction = keys[
            config.KEY_BINDS.pitch[0] - keys[config.KEY_BINDS.pitch[1]]
        ]
        yaw_direction = keys[config.KEY_BINDS.yaw[0] - keys[config.KEY_BINDS.yaw[1]]]
        roll_direction = keys[config.KEY_BINDS.roll[1]] - keys[config.KEY_BINDS.roll[0]]

        movement = (
            self.get_right_vector() * -movement_horizontal
            + self.get_up_vector() * movement_vertical
        )
        self.acceleration = movement * config.side_thrust_force * delta

        brake_force = Vec3(0, 0, 0)
        if movement_vertical == 0:
            brake_force -= (
                self.get_up_vector() * self.velocity.normalize()
            )  # times some brake_force
        if movement_horizontal == 0:
            brake_force -= self.get_right_vector() * self.velocity.normalize()

        # Need to add something to prevent it from rocking

        print(f"Break force: {brake_force}")
        self.acceleration += brake_force * config.side_thrust_force * 1.5 * delta

        self.rotation_acceleration = (
            Vec3(
                pitch_direction,
                roll_direction,
                yaw_direction,
            )
            * config.roll_thrust_force
            * delta
        )

        if keys[config.KEY_BINDS.thrust]:
            self.acceleration += (
                self.get_forward_vector() * config.rear_thrust_force * delta
            )

        if (
            keys[config.KEY_BINDS.shoot]
            and -1 * (self.last_shoot_time - time.time()) > config.SHOOTING_INTERVAL
        ):
            self.shoot()
            self.last_shoot_time = time.time()

    def handle_mouse(self, delta):
        normalized_mouse_position: Vec2 = (Input.mouse - Window.size / 2) / (
            Window.size / 2
        )  # generates a value between -1 and 1 for both axes

        # this treats it as a square, but close enough for now
        print(normalized_mouse_position)
        if (
            abs(normalized_mouse_position.x) < config.virtual_joystick_deadzone
            and abs(normalized_mouse_position.y) < config.virtual_joystick_deadzone
        ) or not config.mouse_movement:
            normalized_mouse_position = Vec2(0, 0)

        normalized_mouse_position * config.roll_thrust_force

        # mouse_rotation = self.get_right_vector() * normalized_mouse_position.x + self.get_up_vector() * normalized_mouse_position.y

        mouse_rotation = Vec3(
            normalized_mouse_position.y,
            0,
            normalized_mouse_position.x,
        )

        self.rotation_acceleration = mouse_rotation

    def shoot(self):
        bullet = Bullet()
        bullet.owner = self.player_id
        bullet.pos = self.pos
        bullet.rotation = self.rotation
        bullet.velocity = self.get_forward_vector() * 30
        bullet.instantiate()

        self.newest_bullet = bullet

    def update_camera_position(self, delta):
        forward = self.get_forward_vector()

        if forward.length == 0:
            return

        Camera.active_camera.pos = (
            forward * -10 + self.pos + self.get_up_vector() * 8
        )  # this does *NOT* work if the camera is rotated, uh oh
        Camera.active_camera.target = forward * 20 + self.pos
