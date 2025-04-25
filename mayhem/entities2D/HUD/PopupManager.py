"""
Contains the PopupManager class and the Popup class
"""
from engine.core_ext.Colour import Colour
from engine.core.Window import Window
from engine.core.Entity import Entity
from engine.core.Entity2D import Entity2D

from pyglet.math import Vec3

import pyglet
import time


class PopupManager(Entity):
    """
    Simple popup manager, lets you create simple popups.
    Inherites Entity to get access to process
    """
    popups = []

    class Popup(Entity2D):
        """
        Simple Popup class. Contains all the necessary info for a popup
        """
        def __init__(self, text, duration, colour):
            """
            Parameters:
                text: The text the popup should have
                duration: How long the popup should stay on the screen. -1 disables the duration
                colour: The colour of the popup
            """
            self.text = text
            self.fontsize = Window.size.y/50
            self.colour = colour
            self.created = time.time()
            self.duration = duration
            super().__init__()

        def user_instantiate(self):
            self.lable = pyglet.text.Label(text = self.text, color=self.colour, batch=self.game_object.UI_batch)

        def prepare_draw(self, delta):
            self.lable.position = Vec3(15, 15 + PopupManager.popups.index(self)*(self.fontsize + 15), 0)

        def on_resize(self):
            self.fontsize = Window.size.y/50

    def create_popup(self, text, duration=10, colour=Colour.YELLOW, position=-1):
        """
        Creates an popup.

        Parameters:
            text: The text the popup should have
            duration: How long the popup should stay on the screen, deafult 10 seconds, -1 disables the duration
            colour: The colour of the text

        returns the popup object
        """
        popup = self.Popup(text, duration=duration, colour=colour)
        popup.instantiate()
        self.popups.insert(position, popup)
        return popup

    def edit_popup(self, popup, text, duration=None, colour=None):
        """
        Edits an popup.

        Parameters:
            text: The text the popup should have
            duration: How long the popup should stay on the screen, deafult 10 seconds, -1 disables the duration
            colour: The colour of the text

        returns the popup object
        """
        popup.text = text
        popup.lable.text = text

        if duration:
            popup.duration = duration
        if colour:
            popup.colour = colour

    def delte_popup(self, popup):
        """
        Deltes an popup.

        Parameters:
            popup: The popup to delete
        """
        self.popups.remove(popup)
        popup.free()

    def get_popup_text(self, popup):
        """
        Return the text of a popup
        """
        return popup.lable.text

    def process(self, delta):
        # Checks if the popup should be deleted
        for popup in self.popups:
            if time.time()-popup.created >= popup.duration and popup.duration != -1:
                self.popups.remove(popup)
                popup.free()

    def prepare_draw(self, delta):
        # Required by the abstract class, but since this in not a renderd entity it is just empyt
        pass
