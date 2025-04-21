"""
( write more later )
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Game import Game
from engine.core.Camera import Camera
from engine.core.Utils import Utils
from engine.core.Window import Window
from engine.core.Input import Input
from engine.core_ext.collision.collision3D.Hitsphere3D import Hitsphere3D

from mayhem.entities.players.Player import Player
from mayhem.entities.Bullet import Bullet
from mayhem.entities2D.HUD.MovementReticle import MovementReticle

import config

from pyglet.math import Vec2, Vec3

import pyglet
import logging
import time

class LocalPlayer(Player):
    instance: Player = None
    
    def user_init(self):
        LocalPlayer.instance = self
        
        self.visible = False

        self.last_shoot_time = 0
        self.new_bullet = 0
        self.score = 0
        self.health = 100

        self.hitboxes = [Hitsphere3D(self.pos, Vec3(0, 0, 0), 2)]

        super().user_init()


    def engine_process(self, delta):
        self.handle_input(delta)
        self.update_camera_position(delta)

        for hitbox in self.hitboxes:
            hitbox.update(self.pos)

        self.check_for_collision()

        logging.debug(f"player pos: {self.pos}, player rotation: {self.rotation}")

    def user_instantiate(self):
        model_scene = pyglet.resource.scene(Utils.get_model_path("test"))

        self.model = model_scene.create_models(batch=Player.game_object.main_batch)[0]

    def handle_input(self, delta):
        keys = Input.keyboard_keys
        
        # generates a value between -1 and 1 for both axes
        standardized_mouse_position: Vec2 = (Input.mouse - Window.size / 2) / (Window.size / 2)
        logging.debug(f"mouse pos: {standardized_mouse_position}")
        
        # caps the length to one
        magnitude = max(1, standardized_mouse_position.length()) # don't divide by values under 1
        normalized_mouse_position = standardized_mouse_position / magnitude
        
        # ignores mouse inputs if the value is too small
        if MovementReticle.is_mouse_inside():
            standardized_mouse_position = Vec2(0, 0)
            normalized_mouse_position = Vec2(0, 0)

        key_movement_vertical = keys[config.KEY_BINDS.vertical[0]] - keys[config.KEY_BINDS.vertical[1]]
        key_movement_horizontal = keys[config.KEY_BINDS.horizontal[0]] - keys[config.KEY_BINDS.horizontal[1]]

        vertical_movement = normalized_mouse_position.y + key_movement_vertical
        horizontal_movement = -normalized_mouse_position.x + key_movement_horizontal

        # flip the horizontal movement if we're not rightside up, this is due to the game using global axes
        if not self.is_rightside_up():
            horizontal_movement = -horizontal_movement
        
        self.rotation_acceleration = Vec3(
            vertical_movement,
            horizontal_movement,
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

    def handle_collision(self, entity):
        if type(entity).__name__ == "Bullet":
            if entity.owner != self.player_id:
                entity.hitboxes = []
                entity.free()
                self.health -= 10
        else:
            print("Hit something")


    def update_camera_position(self, delta):
        forward = self.get_forward_vector()

        if forward.length == 0:
            logging.warning("player does not have a valid forward vector, skipping camera positioning update")

        Camera.active_camera.pos = self.pos
        Camera.active_camera.target = self.pos + forward
        Camera.active_camera.rotation = self.rotation
