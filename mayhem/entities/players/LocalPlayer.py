"""
Contains the LocalPlayer class
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Game import Game
from engine.core.Camera import Camera
from engine.extras.Utils import Utils
from engine.core.Window import Window
from engine.core.Input import Input
from engine.core.Entity3D import Entity3D

from engine.core.Entity3D import Entity3D

from mayhem.entities.players.Player import Player
from mayhem.entities.Bullet import Bullet
from mayhem.entities.obstacles.Obstacle import Obstacle
from mayhem.entities.pickups.Pickup import Pickup
from mayhem.entities2D.HUD.MovementReticle import MovementReticle

import config

from pyglet.math import Vec2, Vec3

import logging
import time
import random
import pyglet


class LocalPlayer(Player):
    """
    The local player, inherits from the generic player class.
    Handles collision and input for the player
    """

    instance: Player = None

    def user_init(self):
        super().user_init()
        LocalPlayer.instance = self

        self.visible = False

        self.last_shoot_time = 0
        self.new_bullet = 0
        self.score = 0
        self.health = 100
        self.fuel = config.STARTING_FUEL

        self.last_bullet_shot_from_right: bool = True

        self.killed_by = -1

    def engine_process(self, delta):
        if self.killed_by != -1:
            return

        if self.fuel > 0:
            self.handle_input(delta)
            if self.acceleration.length() > 0:
                self.fuel -= config.FUEL_RATE*delta
            elif self.rotation_acceleration.length() > 0:
                self.fuel -= config.FUEL_RATE/2*delta

        self.update_camera_position(delta)

        for hitbox in self.hitboxes:
            hitbox.update(self.pos)

        self.check_for_collision(delta)

        # make sure the player doesn't go too far away from the battlefield
        pre_capped_pos = self.pos
        self.pos = Vec3(
            max(-400, min(400, self.pos.x)),
            max(-400, min(400, self.pos.y)),
            max(-400, min(400, self.pos.z))
        )
        if pre_capped_pos != self.pos:
            self.velocity = -self.velocity
            self.rotation = -self.rotation
            Player.game_object.popupmanager.create_popup("A mysterious force is stopping you from going any farther.")
        
        if config.PLAY_SFX:
            listener = pyglet.media.get_audio_driver().get_listener()
            listener._set_position(self.pos)
            listener.forward_orientation = tuple(self.get_forward_vector())
            listener.up_orientation = tuple(-self.get_up_vector())

    def handle_input(self, delta):
        """
        Handles the input.
        """
        if Input.is_typing:
            return
        keys = Input.keyboard_keys

        # generates a value between -1 and 1 for both axes
        standardized_mouse_position: Vec2 = (Input.mouse - Window.size / 2) / (Window.size / 2)

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
            self._shoot()
            self.last_shoot_time = time.time()

    def _shoot(self):
        """
        Creates a bullet.
        """
        bullet = Bullet()
        
        self.last_bullet_shot_from_right = not self.last_bullet_shot_from_right
        if self.last_bullet_shot_from_right:
            bullet.pos = self.pos + self.get_right_vector() * 1.5
        else:
            bullet.pos = self.pos - self.get_right_vector() * 1.5

        bullet.owner = self.player_id
        bullet.rotation = self.rotation
        bullet.velocity = self.velocity + self.get_forward_vector() * config.BULLET_SPEED
        bullet.instantiate()
        
        if config.PLAY_SFX:
            source = pyglet.media.load(random.choice(self.laser_sfx), streaming=True)
            self.audio_player.position = self.pos
            self.audio_player.queue(source)
            self.audio_player.play()

        self.new_bullet = 1  # Informs the game loop that a new bullet was created and it should be reported to the server

    def _respawn(self):
        """
        Respawns the player
        """
        self.score -= 1
        self.health = 100
        self._spawn()
        self._spawn()

    def _spawn(self):
        """
        Spawns the player
        """
        self.pos = Utils.get_random_normalized_3D_vector() * 300
        self.velocity = Vec3()
        self.rotation = Vec3()

    def handle_collision(self, entity: Entity3D, delta: float):
        """
        Handles collision
        Gets called on every collision.

        Parameters:
            entity: The entity it collided with
            delta: delta time
        """
        # If it hit a bullet
        if isinstance(entity, Bullet):
            if entity.owner != self.player_id:
                self.health -= 25
                logging.info(f"shot by {entity.owner}")
                entity.free()

        # If it hit an obstacle
        elif isinstance(entity, Obstacle) or isinstance(entity, Player):
            if self.velocity.length() > 0 or entity.velocity.length() > 0:
                self.health -= max(10, self.velocity.length()) * 0.5 + max(10, entity.velocity.length()) * 0.5
                self._spawn()

        # If it hit a pickup
        elif isinstance(entity, Pickup):
            entity.picked_up(self)
            return

        # Is dead?
        if self.health <= 0:
            # Makes sure the correct player gets credit for the kill
            if isinstance(entity, Bullet):
                self.killed_by = entity.owner
            elif isinstance(entity, Player):
                self.killed_by = entity.player_id
            else:
                self.killed_by = -1

            self._respawn()

    def update_camera_position(self, delta):
        forward = self.get_forward_vector()

        if forward.length == 0:
            logging.warning("player does not have a valid forward vector, skipping camera positioning update")

        Camera.active_camera.pos = self.pos
        Camera.active_camera.target = self.pos + forward
        Camera.active_camera.rotation = self.rotation

    def get_gravity(self):
        """
        Calculates the gravity acting on the player.
        Using Newtons gravity law.
        """
        g = Vec3()
        for entity in Entity3D.all_3D_entities:
            d = entity.pos - self.pos
            if d.length() == 0:
                continue
            F = (config.GRAVITATIONAL_CONSTANT * self.mass*entity.mass)/d.length()**2

            g += d.normalize()*F

        return g
