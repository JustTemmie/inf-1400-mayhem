import abc


class Hitarea(abc.ABC):
    def __init__(self, type: str):
        self.type = type

    @abc.abstractmethod
    def colliding_with(self, area: "Hitarea"):
        pass

    @abc.abstractmethod
    def update_object(self, object_pos, object_rot):
        pass
