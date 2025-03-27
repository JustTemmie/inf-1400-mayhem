from engine.core_ext.Netwoking import Networking


class MayhemNetworking(Networking):
    def encode(self, data: tuple) -> bytes:
        out = ""
        for i in data:
            out += f" {i}"
        return out[1:].encode()

    def decode(self, data: bytes) -> tuple:
        return tuple(data.decode().split(" "))
