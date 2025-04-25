"""
Contains the mayhem class
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Game import Game
from engine.core_ext.Netwoking import Networking
import engine.extras.logger # this is just to init the module, do not remove even though it's unused

from engine.core_ext.collision.collision3D.Hitbox3D import Hitbox3D
from engine.extras.Utils import Utils

from mayhem.entities.players.Player import Player
from mayhem.entities.pickups.Battery import Battery
from mayhem.entities.obstacles.Planet import Planet
from mayhem.entities.ExampleObject import ExampleObject

from mayhem.Packet import Packet

from mayhem.entities.players.LocalPlayer import LocalPlayer
from mayhem.entities.players.RemotePlayer import RemotePlayer
from mayhem.entities.Bullet import Bullet

from mayhem.entities2D.HUD.MovementArrow import MovementArrow
from mayhem.entities2D.HUD.MovementReticle import MovementReticle
from mayhem.entities2D.HUD.ScoreCounter import ScoreCounter
from mayhem.entities2D.HUD.HealthCounter import HealthCounter
from mayhem.entities2D.HUD.FuelCounter import FuelCounter
from mayhem.entities2D.HUD.PopupManager import PopupManager

import config

from pyglet.math import Vec3

import typing
import logging


class Mayhem(Game):
    """
    The main game class.
    Spawns all the objects in the game, except bullets.
    """

    def init(self):
        """
        Runs once at the start of the game.
        """
        self.player: LocalPlayer
        self.other_players: typing.Dict[int, RemotePlayer] = {}

        print("LOADING...")
        self.spawn_local_player()
        self.spawn_remote_players()
        self.spawn_obstacles()
        self.spawn_hud()

        self.music_manager.fade_to("assets/music/gravity_turn_calm.ogg")
        self.faded = False

        self.last_spawned_battery_time: float = -50

    def user_engine_process(self, delta):
        # this music check should probably just run when the player goes from the main menu to the game
        # or, we could fade to the action music whenever another player is nearby, though i'm not sure that would work well
        if self.time_elapsed > 20 and not self.faded:
            self.faded = True
            self.music_manager.fade_to("assets/music/gravity_turn_action.ogg")

        self._handle_network_input()
        self._send_update()

        if self.time_elapsed > self.last_spawned_battery_time + config.BATTERY_SPAWN_COOLDOWN:
            self.last_spawned_battery_time = self.time_elapsed

            battery = Battery()
            battery.spawn(220)
            battery.instantiate()

    def spawn_hud(self):
        """
        Spawns all the HUD entities
        """
        MovementArrow().instantiate()
        MovementReticle().instantiate()
        ScoreCounter().instantiate()
        HealthCounter().instantiate()
        FuelCounter().instantiate()

        self.popupmanager = PopupManager()
        self.popupmanager.instantiate()

    def spawn_local_player(self):
        """
        Spawns the local player
        """
        self.player = LocalPlayer()
        self.player._spawn()
        self.player.instantiate()

    def spawn_remote_players(self):
        """
        Starts listening to server.
        """
        self.networking = Networking(
            config.SERVER_PORT, config.SERVER_ADDRESS
        )  # FIXME: Should be changed later. Port and address should be a user input
        if self.networking.connected:
            self.networking.start_listen()  # Creates a thread that listens to the server.
            self.networking.send(Packet.player_to_packet(self.player))

    def spawn_obstacles(self):
        """
        Spawns the planet
        """
        planet = Planet()
        planet.pos = Vec3(0, 0, 0)
        planet.instantiate()

    def _send_update(self):
        """
        Sends all the relevent info about the player to the server
        """
        if self.networking.connected:
            self.networking.send(Packet.player_to_packet(self.player))
            self.player.new_bullet = 0
            self.player.killed_by = -1

    def _handle_network_input(self):
        """
        Empties the network queue and handles all the requests
        """
        self.networking.lock.acquire()  # Locks the queue so that two threads can not use it at the same time
        while not self.networking.q.empty():
            data = self.networking.q.get()
            packet = Packet.decode(data)
            if self.player.player_id == 0:
                self.player.player_id = packet.packet.to_id
            if packet.packet.from_id not in self.other_players:
                logging.info(f"Player with ID {packet.packet.from_id} joined")
                self.popupmanager.create_popup(f"Player with ID {packet.packet.from_id} joined")
                self.other_players[packet.packet.from_id] = RemotePlayer()
                self.other_players[packet.packet.from_id].instantiate()
            else:
                if not self.other_players[packet.packet.from_id]:
                    self.other_players[packet.packet.from_id] = RemotePlayer()
                    self.other_players[packet.packet.from_id].instantiate()

            self.other_players[packet.packet.from_id].update_pos(packet)

            if packet.packet.new_bullet:
                b = Bullet()
                b.owner = packet.packet.from_id
                b.pos = packet.packet.player_pos
                b.rotation = packet.packet.player_rotation
                b.velocity = self.other_players[packet.packet.from_id].get_forward_vector()*config.BULLET_SPEED
                b.instantiate()

            if packet.packet.killed_by >= 0:
                killed_player = self.other_players[packet.packet.from_id]
                self.other_players[packet.packet.from_id] = None

                killed_player.free()

                if packet.packet.killed_by == self.player.player_id:
                    self.player.score += 1
                # Server id, this just means that the player dissconected
                elif packet.packet.killed_by == 0:
                    self.other_players.pop(packet.packet.from_id)
                    logging.info(f"Player with ID {packet.packet.from_id} disconnected")
                    self.popupmanager.create_popup(f"Player with ID {packet.packet.from_id} disconnected")

        self.networking.lock.release()
