"""
Contains the Hitarea class

authors: BAboe
"""
import abc

from pyglet.math import Vec3


class Hitarea(abc.ABC):
    """
    Parent class of all Hitboxes/Hitspheres.
    Contains also the collision function.
    """
    def __init__(self):
        pass

    # GJK algorithem, https://youtu.be/ajv46BSqcK4?si=4tmuvwAcWBDa-Ch0
    def colliding_with(self, area: "Hitarea"):
        """
        Checks if this hitarea is colliding wiht "area" hitarea

        Parameters:
            area: The area you want to check if you are colliding with

        Returns:
            Bool: True if colliding, False if not
        """
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
        """
        Returns the minkowsky difference of the two areas

        Parameters:
            area: The area you want the minkowsky difference with
            direction: The direction you want the minkowsky difference
        """
        return self.furthestPoint(direction) - area.furthestPoint(-direction)

    def _handleSimplex(self, simplex, direction):
        """
        Finds the next point on the simplex, and if origo is in the current simplex

        Parameters:
            simplex: The simplex to operate on
            direction: Current direction

        Returns:
            (Vec3, bool): New direction, if origo is in the simplex
        """
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
        """
        Updates the position, and potentialy other parameters.

        Parameters:
            object_pos: The position of the object the hitarea is associated with
        """
        pass

    @abc.abstractmethod
    def furthestPoint(self, d):
        """
        The furthest point in a given direction

        Parameters:
            d: The given direction

        Returns:
            Vec3: The furthest point
        """
        pass

    @abc.abstractmethod
    def center(self):
        """
        Returns the center of the area
        """
        pass
