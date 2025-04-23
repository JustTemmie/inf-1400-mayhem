"""
Colour constants :3
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

from collections import namedtuple

Colour = namedtuple("colour", ("r", "g", "b"))

Colour.RED = Colour(255, 0, 0)
Colour.GREEN = Colour(0, 255, 0)
Colour.BLUE = Colour(0, 0, 255)
Colour.YELLOW = Colour(255, 255, 0)
Colour.CYAN = Colour(0, 255, 255)
Colour.MAGENTA = Colour(255, 0, 255)
Colour.ORANGE = Colour(255, 192, 0)
Colour.PURPLE = Colour(192, 0, 192)
Colour.WHITE = Colour(255, 255, 255)
Colour.BLACK = Colour(0, 0, 0)
Colour.YELLOW = Colour(255, 239, 0)
Colour.GREY = Colour(128, 128, 128)

Colour.CELESTE = Colour(178, 255, 255)
Colour.PALE_BROWN = Colour(155, 118, 83)
Colour.GIRL_SCOUT_SCREEN = Colour(0, 174, 88)