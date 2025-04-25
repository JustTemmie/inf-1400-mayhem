"""
Contains the Packet class
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
    """
    A utility class that represents the network packet.
    """

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
        killed_by=-1,
        message=""
    ):
        """
        Creates a namedtuple with all the packets information
        Parameters:
            from_id: The ID of the client that sent the package.
            to_id: The ID of the client that recived the packet. This is set by server, so can be whatever when sending.
            player_pos: Player_Pos
            player_velocity: The player velocity
            player_acceleration: The player acceleration
            player_rotation: The player rotation
            player_rotation_velocity: The player rotation velocity
            player_rotation_acceleration: The player rotation acceleration
        """
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
                "killed_by",
                "message"
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
            killed_by,
            message
        )

    def encode(self) -> bytes:
        """
        Encodes the packet

        Returns the encoded packet.
        """
        out = ""
        if self.packet.message == "":
            out = "0"
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
            return out.encode()
        else:
            out = f"1 {self.packet.from_id} {self.packet.to_id} {self.packet.message}"
            return out.encode()

    @classmethod
    def decode(self, data: bytes) -> "Packet":
        """
        Decodes a packet.

        Parameters:
            data: The data to decode

        Returns:
            A Packet instance with the decoded data.
        """
        decoded_data = data.decode().split(" ")
        # Please read README in server
        try:
            if int(decoded_data[0]) == 0:
                packet = Packet(
                    int(decoded_data[1]),
                    int(decoded_data[2]),
                    Vec3(
                        float(decoded_data[3]), float(decoded_data[4]), float(decoded_data[5])
                    ),
                    Vec3(
                        float(decoded_data[6]), float(decoded_data[7]), float(decoded_data[8])
                    ),
                    Vec3(
                        float(decoded_data[9]), float(decoded_data[10]), float(decoded_data[11])
                    ),
                    Vec3(
                        float(decoded_data[12]),
                        float(decoded_data[13]),
                        float(decoded_data[14]),
                    ),
                    Vec3(
                        float(decoded_data[15]),
                        float(decoded_data[16]),
                        float(decoded_data[17]),
                    ),
                    Vec3(
                        float(decoded_data[18]),
                        float(decoded_data[19]),
                        float(decoded_data[20]),
                    ),
                    int(decoded_data[21]),
                    int(decoded_data[22]),
                )
            else:
                packet = Packet(from_id=decoded_data[1], to_id=decoded_data[2], message=" ".join(decoded_data[3:]))
        except Exception as e:
            logging.error("Bad packet :(")
            print(e)
            return None
        return packet

    @classmethod
    def player_to_packet(self, p: Player) -> "Packet":
        """
        Makes a packet from a player.

        Parameters:
            p: The player

        Returns a packet instance with the player data.
        """
        packet = Packet(
            p.player_id,
            0,
            p.pos,
            p.velocity,
            p.acceleration,
            p.rotation,
            p.rotation_velocity,
            p.rotation_acceleration,
            p.new_bullet,
            p.killed_by,
            ""
        )

        return packet
