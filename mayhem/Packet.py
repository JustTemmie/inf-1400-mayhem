"""
< write some stuff >
Authors: BAaboe (i'll replace names at handin)
"""

from engine.core_ext.Netwoking import Networking

from mayhem.entities.players.Player import Player
from mayhem.entities.Bullet import Bullet

import logging

from pyglet.math import Vec3

import typing

from collections import namedtuple


class Packet:
    def __init__(
        self,
        from_id=0,
        to_id=0,
        player_pos=Vec3(0, 0, 0),
        player_velocity=Vec3(0, 0, 0),
        player_acceleration=Vec3(0, 0, 0),
        player_rotation=Vec3(0, 0, 0),
        player_rotation_velocity=Vec3(0, 0, 0),
        player_rotation_acceleration=Vec3(0, 0, 0),
        new_bullet=0,
        killed_by=0,
    ):

        PacketTuple = namedtuple(
            "Packet",
            [
                "from_id",
                "to_id",
                "player_pos",
                "player_velocity",
                "player_acceleration",
                "player_rotation",
                "player_rotation_velocity",
                "player_rotation_acceleration",
                "new_bullet",
                "killed_by"
            ],
        )

        self.packet = PacketTuple(
            from_id,
            to_id,
            player_pos,
            player_velocity,
            player_acceleration,
            player_rotation,
            player_rotation_velocity,
            player_rotation_acceleration,
            new_bullet,
            killed_by
        )

    def encode(self) -> bytes:
        out = ""
        for i in self.packet:
            out += " "
            if isinstance(i, Vec3):
                out += str(i.x)
                out += " "
                out += str(i.y)
                out += " "
                out += str(i.z)
            else:
                out += str(i)
        return out[1:].encode()

    @classmethod
    def decode(self, data: bytes) -> "Packet":
        decoded_data = data.decode().split(" ")
        # Please read README in server
        try:
            packet = Packet(
                int(decoded_data[0]),
                int(decoded_data[1]),
                Vec3(
                    float(decoded_data[2]), float(decoded_data[3]), float(decoded_data[4])
                ),
                Vec3(
                    float(decoded_data[5]), float(decoded_data[6]), float(decoded_data[7])
                ),
                Vec3(
                    float(decoded_data[8]), float(decoded_data[9]), float(decoded_data[10])
                ),
                Vec3(
                    float(decoded_data[11]),
                    float(decoded_data[12]),
                    float(decoded_data[13]),
                ),
                Vec3(
                    float(decoded_data[14]),
                    float(decoded_data[15]),
                    float(decoded_data[16]),
                ),
                Vec3(
                    float(decoded_data[17]),
                    float(decoded_data[18]),
                    float(decoded_data[19]),
                ),
                int(decoded_data[20]),
                int(decoded_data[21]),
            )
        except:
            logging.error("Bad packet :(")
            return None
        return packet

    @classmethod
    def player_to_packet(self, p: Player, new_bullet=0, killed_by=0) -> tuple:
        packet = Packet(
            p.player_id,
            0,
            p.pos,
            p.velocity,
            p.acceleration,
            p.rotation,
            p.rotation_velocity,
            p.rotation_acceleration,
            new_bullet,
            killed_by
        )

        return packet
