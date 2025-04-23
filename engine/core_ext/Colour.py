"""
Colour constants :3
Authors: BAaboe, JustTemmie (i'll replace names at handin)
"""

class Colour:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 192, 0)
    PURPLE = (192, 0, 192)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 239, 0)
    GREY = (128, 128, 128)
    CELESTE = (178, 255, 255)
    PALE_BROWN = (155, 118, 83)
    GIRL_SCOUT_SCREEN = (0, 174, 88)
    
    # this isn't stupid, trust, it's very important!!!!
    def __init__(self, r, g, b) -> tuple:
        return (r, g ,b)