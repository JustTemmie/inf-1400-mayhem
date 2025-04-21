"""
Generic hitarea using the GJK algorithem
authors: BAboe
"""
import abc

from pyglet.math import Vec3


class Hitarea(abc.ABC):
    def __init__(self, type: str):
        self.type = type

    # GJK algorithem, https://youtu.be/ajv46BSqcK4?si=4tmuvwAcWBDa-Ch0
    def colliding_with(self, area: "Hitarea"):
        direction = (self.center()-area.center()).normalize()

        A = self._support(area, direction)
        simplex = [A]
        direction = -A.normalize()

        while True:
            A = self._support(area, direction)
            if A.dot(direction) < 0:
                return False
            simplex.append(A)

            direction, contains = self._handleSimplex(simplex, direction)
            if contains:
                return True

    def _support(self, area, direction):
        return self.furthestPoint(direction) - area.furthestPoint(-direction)

    def _handleSimplex(self, simplex, direction):
        if len(simplex) == 2:
            B, A = simplex
            AB, AO = B - A, -A
            ABperp = AB.cross(AO).cross(AB)
            return (ABperp, False)
        C, B, A = simplex
        AB, AC, AO = B - A, C - A, -A
        ABperp = AC.cross(AB).cross(AB)
        ACperp = AB.cross(AC).cross(AC)

        if ABperp.dot(AO) > 0:
            simplex.remove(C)
            return (ABperp, False)
        elif ACperp.dot(AO) > 0:
            simplex.remove(B)
            return (ACperp, False)
        return (0, True)

    @abc.abstractmethod
    def update(self, object_pos):
        pass

    @abc.abstractmethod
    def furthestPoint(self, d):
        pass

    @abc.abstractmethod
    def center(self):
        pass
