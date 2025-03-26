# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

from engine.core.Game import Game
from engine.core_ext.Entity import Entity

from mayhem.entities.Player import Player

from mayhem.MayhemNetworking import MayhemNetworking

import pyglet
import config

class Mayhem(Game):
    def init(self):
        # Player().instantiate(self)

        self.mn = MayhemNetworking(config.SERVER_PORT, config.SERVER_TEST_ADDRESS) # FIXME: Should be changed later. Port and address should be a user input
        if self.mn.connected:
            self.mn.start_listen()  # Creates a thread that listens to the server.
            self.mn.send(b"1 1 1") # FIXME: Remove

    def user_engine_process(self, delta):
        self._handle_network_input()
        pass

    def _handle_network_input(self):
        self.mn.lock.acquire()  # Locks the queue so that two threads do not use it at the same time
        while not self.mn.q.empty():
            data = self.mn.decode(self.mn.q.get())
            # TODO: Handle each request from the server
        self.mn.lock.release()
