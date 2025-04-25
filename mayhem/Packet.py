"""
Contains the Packet class
Authors: BAaboe (i'll replace names at handin)
"""

from mayhem.entities.players.Player import Player

import logging

from pyglet.math import Vec3

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
        """
        Encodes the packet

        Returns the encoded packet.
        """
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
            p.killed_by
        )

        return packet
