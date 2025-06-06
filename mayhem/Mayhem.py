"""
Contains the mayhem class
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Game import Game
from engine.core_ext.Netwoking import Networking
from engine.core.Input import Input
import engine.extras.logger # this is just to init the module, do not remove even though it's unused

from mayhem.entities.pickups.Battery import Battery
from mayhem.entities.obstacles.Planet import Planet

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
        self.spawn_obstacles()
        self.spawn_hud()
        self.spawn_remote_players()

        self.last_spawned_battery_time: float = -50

        self.window.push_handlers(self.on_text)

    def user_engine_process(self, delta):
        # play calm or action music, depending on if you're alone or not
        if config.PLAY_MUSIC:
            if len(self.other_players) == 0 and self.music_manager.currently_playing != "assets/music/gravity_turn_calm.ogg":
                self.music_manager.fade_to("assets/music/gravity_turn_calm.ogg")
            elif len(self.other_players) >= 1 and self.music_manager.currently_playing != "assets/music/gravity_turn_action.ogg":
                self.music_manager.fade_to("assets/music/gravity_turn_action.ogg")
        
        self._handle_network_input()
        self._send_update()

        if self.time_elapsed > self.last_spawned_battery_time + config.BATTERY_SPAWN_COOLDOWN:
            self.last_spawned_battery_time = self.time_elapsed

            battery = Battery()
            battery.spawn(230)
            battery.instantiate()

    def on_text(self, text):
        if text == "\r" and not Input.is_typing:
            Input.is_typing = True
            self.message = self.popupmanager.create_popup(text="", duration=-1, position=0)
            return

        if Input.is_typing:
            if text == "\r":
                Input.is_typing = False
                message = self.popupmanager.get_popup_text(self.message)
                self._send_message(message)
                self.popupmanager.delte_popup(self.message)
                self.message = None
                self.popupmanager.create_popup(f"ID {self.player.player_id}: {message}")
            else:
                message = self.popupmanager.get_popup_text(self.message)
                message += text
                self.popupmanager.edit_popup(self.message, message)

    def _send_message(self, message):
        if self.networking.connected and self.player.player_id:
            self.networking.send(Packet(from_id=self.player.player_id, message=message))


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

        print("Connecting to server...")
        self.networking = Networking(
            config.SERVER_PORT, config.SERVER_ADDRESS
        )  # FIXME: Should be changed later. Port and address should be a user input
        if self.networking.connected:
            print("Connected to server!")
            self.networking.start_listen()  # Creates a thread that listens to the server.
            self.networking.send(Packet.player_to_packet(self.player))
        else:
            print("Failed connecting to server, single player session started...")
        
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
        if self.networking.connected and self.player.player_id != 0:
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
            if packet.packet.message:
                self.popupmanager.create_popup(f"ID {packet.packet.from_id}: {packet.packet.message}")
                continue

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
                self.other_players[packet.packet.from_id].shoot(packet)

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
