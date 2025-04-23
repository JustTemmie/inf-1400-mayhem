"""
( write more later )
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from engine.core.Game import Game
from engine.core_ext.Netwoking import Networking
import engine.extras.logger # this is just to init the module, do not remove even though it's unused

from engine.core_ext.collision.collision3D.Hitbox3D import Hitbox3D

from mayhem.entities.players.Player import Player
from mayhem.entities.pickups.Battery import Battery
from mayhem.entities.obstacles.Planet import Planet
from mayhem.entities.obstacles.ExampleObject import ExampleObject

from mayhem.Packet import Packet

from mayhem.entities.players.LocalPlayer import LocalPlayer
from mayhem.entities.players.RemotePlayer import RemotePlayer
from mayhem.entities.Bullet import Bullet

from mayhem.entities2D.HUD.MovementArrow import MovementArrow
from mayhem.entities2D.HUD.MovementReticle import MovementReticle
from mayhem.entities2D.HUD.ScoreCounter import ScoreCounter
from mayhem.entities2D.HUD.HealthCounter import HealthCounter
from mayhem.entities2D.HUD.FuelCounter import FuelCounter


from pyglet.math import Vec3

import typing
import pyglet
import config
import logging


class Mayhem(Game):
    def init(self):
        self.player: LocalPlayer
        self.other_players: typing.Dict[int, RemotePlayer] = {}
        
        self.spawn_local_player()
        self.spawn_remote_players()
        self.spawn_test_objects()
        self.spawn_hud()
        
        self.last_spawned_battery_time: float = -50
    
    def user_engine_process(self, delta):
        self._handle_network_input()
        self._send_update()
        
        if self.time_elapsed > self.last_spawned_battery_time + 20:
            self.last_spawned_battery_time = self.time_elapsed
            
            if Battery.current_battery:
                Battery.current_battery.free()
                Battery.current_battery = None

            battery = Battery()
            battery.pos = Vec3(2, -5, 2)
            battery.instantiate()
        
    
    
    def spawn_hud(self):
        MovementArrow().instantiate()
        MovementReticle().instantiate()
        ScoreCounter().instantiate()
        HealthCounter().instantiate()
        FuelCounter().instantiate()
    
    def spawn_local_player(self):
        self.player = LocalPlayer()
        self.player.pos = Vec3(2, -10, 0)
        self.player.instantiate()
    
    def spawn_remote_players(self):
        self.networking = Networking(
            config.SERVER_PORT, config.SERVER_ADDRESS
        )  # FIXME: Should be changed later. Port and address should be a user input
        if self.networking.connected:
            self.networking.start_listen()  # Creates a thread that listens to the server.
            self.networking.send(Packet.player_to_packet(self.player))

    def spawn_test_objects(self):
        player = Player()
        player.pos = Vec3(-5, 0, 0)
        player.instantiate()

        player = Player()
        player.pos = Vec3(-5, 0, 15)
        player.instantiate()

        planet = Planet()
        planet.pos = Vec3(15, 140, 70)
        planet.instantiate()

        for i in range(25):
            object = ExampleObject()
            object.pos = Vec3(0, 0, i * 2 - 50)
            object.hitboxes.append(Hitbox3D(object.pos, object.rotation, Vec3(1, 1, 1), Vec3()))
            object.instantiate()

    def _send_update(self):
        if self.networking.connected:
            self.networking.send(Packet.player_to_packet(self.player,
                                                         self.player.new_bullet,
                                                         self.player.killed_by))
            self.player.new_bullet = 0
            self.player.killed_by = -1

    def _handle_network_input(self):
        self.networking.lock.acquire()  # Locks the queue so that two threads can not use it at the same time
        while not self.networking.q.empty():
            data = self.networking.q.get()
            packet = Packet.decode(data)
            if self.player.player_id == 0:
                self.player.player_id = packet.packet.to_id
            if packet.packet.from_id not in self.other_players:
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
                self.other_players.pop(packet.packet.from_id)

                killed_player.free()

                if packet.packet.killed_by == self.player.player_id:
                    self.player.score += 1
                # Server id, this just means that the player dissconected
                elif packet.packet.killed_by == 0:
                    logging.info(f"Player with ID {packet.packet.from_id} disconnected")

        self.networking.lock.release()
