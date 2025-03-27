# adds the project root to the path, this is to allow importing other files in an easier manner
# if you know a better way of doing this, please tell me!
if __name__ == "__main__":
    import sys
    sys.path.append(".")

from engine.core.Game import Game
from engine.core_ext.Entity import Entity

from mayhem.entities.Player import Player
from mayhem.entities.ExampleObject import ExampleObject

from mayhem.MayhemNetworking import MayhemNetworking

import pyglet
import pyglet.window.key
import config

class Mayhem(Game):
    def init(self):
        self.player = Player()
        self.player.pos = pyglet.math.Vec3(5, 0, 0)
        self.player.instantiate(self)

        self.spawn_test_objects()
        
        self.window.event("on_key_press")(self.player.on_key_press)
        self.window.event("on_key_release")(self.player.on_key_release)

        self.mn = MayhemNetworking(config.SERVER_PORT, config.SERVER_TEST_ADDRESS) # FIXME: Should be changed later. Port and address should be a user input
        if self.mn.connected:
            self.mn.start_listen()  # Creates a thread that listens to the server.
            self.mn.send(b"1 1 1") # FIXME: Remove

    def spawn_test_objects(self):
        player = Player()
        player.pos = pyglet.math.Vec3(-5, 0, 0)
        player.instantiate(self)
        
        player = Player()
        player.pos = pyglet.math.Vec3(-5, 0, 15)
        player.instantiate(self)
        
        ExampleObject().instantiate(self)

    def user_engine_process(self, delta):

        self._handle_network_input()
        pass

    def _handle_network_input(self):
        self.mn.lock.acquire()  # Locks the queue so that two threads do not use it at the same time
        while not self.mn.q.empty():
            data = self.mn.decode(self.mn.q.get())
            # TODO: Handle each request from the server
        self.mn.lock.release()


