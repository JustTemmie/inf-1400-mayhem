"""
This module just assists in the game's ability to switch between music tracks
Authors: JustTemmie (i'll replace names at handin)
"""

import pyglet

class MusicManager:
    """
    Stores two music players, and gives the game the ability to crossfade between them
    """

    # since there's only ever intended to be one player
    # this easily lets us reference the player from something like a button or the player itself
    current_manager = None

    def __init__(self):
        MusicManager.current_manager = self

        self.player_1 = pyglet.media.Player()
        self.player_2 = pyglet.media.Player()

        self.main_player = self.player_1

        self.player_1.volume = 0.5
        self.player_2.volume = 0

        self.player_1.loop = True
        self.player_2.loop = True

        self.fading: bool = False

    def _fade_to_with_player(self, path: str, player: pyglet.media.Player):
        """
        Load a track into a given player, and start playing it at 0 volume

        Not intended to be used outside of the engine
        """
        source = pyglet.media.load(path, streaming=True)
        player.next_source()
        player.queue(source)
        player.volume = 0
        player.play()
        self.fading = True

    def fade_to(self, path: str):
        """
        Start fading to a new music track
        """
        if self.main_player == self.player_1:
            self._fade_to_with_player(path, self.player_2)
        else:
            self._fade_to_with_player(path, self.player_1)
        
    
    def process_fading(self):
        """
        Called once every tick to handle fading
        """
        if not self.fading:
            return

        if self.main_player == self.player_1:
            self.player_1.volume -= 0.003
            self.player_2.volume += 0.003
        
        elif self.main_player == self.player_2:
            self.player_1.volume += 0.003
            self.player_2.volume -= 0.003
        
        
        if self.player_1.volume >= 0.48 and self.main_player != self.player_1:
            self.player_2.pause()

            self.main_player = self.player_1
            self.main_player.volume = 0.5
            self.main_player.loop = True
            self.fading = False
        
        elif self.player_2.volume >= 0.48 and self.main_player != self.player_2:
            self.player_1.pause()
            
            self.main_player = self.player_2
            self.main_player.volume = 0.5
            self.main_player.loop = True
            self.fading = False

    

# for testing
if __name__ == "__main__":
    music = MusicManager()
    music.play("assets/music/gravity_turn_calm.wav")