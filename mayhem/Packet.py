from engine.core_ext.Netwoking import Networking

from mayhem.entities.players.Player import Player
from mayhem.entities.Bullet import Bullet

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
        bullet_pos=Vec3(0, 0, 0),
        bullet_velocity=Vec3(0, 0, 0),
        bullet_acceleration=Vec3(0, 0, 0),
        bullet_rotation=Vec3(0, 0, 0),
        bullet_rotation_velocity=Vec3(0, 0, 0),
        bullet_rotation_acceleration=Vec3(0, 0, 0),
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
                "bullet_pos",
                "bullet_velocity",
                "bullet_acceleration",
                "bullet_rotation",
                "bullet_rotation_velocity",
                "bullet_rotation_acceleration",
                "killed_by",
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
            bullet_pos,
            bullet_velocity,
            bullet_acceleration,
            bullet_rotation,
            bullet_rotation_velocity,
            bullet_rotation_acceleration,
            killed_by,
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
        if len(decoded_data) != 39:
            raise TypeError("Bad packet:(")
        # Please read README in server
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
            Vec3(
                float(decoded_data[20]),
                float(decoded_data[21]),
                float(decoded_data[22]),
            ),
            Vec3(
                float(decoded_data[23]),
                float(decoded_data[24]),
                float(decoded_data[25]),
            ),
            Vec3(
                float(decoded_data[26]),
                float(decoded_data[27]),
                float(decoded_data[28]),
            ),
            Vec3(
                float(decoded_data[29]),
                float(decoded_data[30]),
                float(decoded_data[31]),
            ),
            Vec3(
                float(decoded_data[32]),
                float(decoded_data[33]),
                float(decoded_data[34]),
            ),
            Vec3(
                float(decoded_data[35]),
                float(decoded_data[36]),
                float(decoded_data[37]),
            ),
            int(decoded_data[38]),
        )
        return packet

    @classmethod
    def player_to_packet(self, p: Player, b: Bullet = Bullet(), killed_by=0) -> tuple:
        packet = Packet(
            p.player_id,
            0,
            p.pos,
            p.velocity,
            p.acceleration,
            p.rotation,
            p.rotation_velocity,
            p.rotation_acceleration,
            b.pos,
            b.velocity,
            b.acceleration,
            b.rotation,
            b.rotation_velocity,
            b.rotation_acceleration,
            killed_by,
        )

        return packet
