# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

from engine.core.Game import Game
from engine.core_ext.Entity import Entity

from mayhem.entities.Player import Player

import pyglet
import config

class Mayhem(Game):
    def init(self):
        Player().instantiate(self)
