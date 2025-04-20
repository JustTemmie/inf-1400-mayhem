"""
Generic hitarea using the GJK algorithem
OBS: This is not tested yet
authors: BAboe
"""
import abc

from pyglet.math import Vec3


class Hitarea(abc.ABC):
    def __init__(self, type: str):
        self.type = type

    # GJK algorithem, https://youtu.be/ajv46BSqcK4?si=4tmuvwAcWBDa-Ch0
    def colliding_with(self, area: "Hitarea"):
        direction = Vec3(1, 0, 0)

        A = self.support(direction)
        simplex = [A]
        direction = -A

        while True:
            A = self.support(direction) - self.support(-direction)
            if A.dot(direction) < 0:
                return False
            simplex.append(A)

            direction, contains = self._handleSimplex(simplex, direction)
            if contains:
                return True

    def _handleSimplex(simplex, direction):
        if len(simplex):
            B, A = simplex
            AB, AO = B - A, -A
            ABperp = AB.cross(AO).cross(AB)
            return (ABperp, False)
        C, B, A = simplex
        AB, AC, AO = B - A, C - A, -A
        ABperp = AC.cross(AB).cross(AB)
        ACperp = AB.crodd(AC).crodd(AC)

        if ABperp.dot(AO) > 0:
            simplex.remove(C)
            return (ABperp, False)
        elif ACperp.dot(AO) > 0:
            simplex.remove(C)
            return (ACperp, False)
        return True

    @abc.abstractmethod
    def update(self, object_pos):
        pass

    @abc.abstractmethod
    def support(self, d):
        pass
