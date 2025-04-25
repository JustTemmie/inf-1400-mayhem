"""
This module just contains some utility functions to be used elsewhere
Authors: JustTemmie (i'll replace names at handin)
"""

import pyglet

class Utils:
    """
    Not intended to be turned into an object.
    """

    @staticmethod
    def print_system_info() -> None:
        """
        Print relevant system info
        """
        result = "\n".join(
            [
                f"GPU Vendor: {pyglet.gl.gl_info.get_vendor()}",
                f"GPU Renderer: {pyglet.gl.gl_info.get_renderer()}",
                f"OpenGL version supported: {pyglet.gl.gl_info.get_version_string()}",
            ]
        )
        print(result)

    @staticmethod
    def get_model_path(model: str) -> str:
        """
        Shorthand for fetching model pathes
        """
        return f"assets/models/{model}/{model}.obj"


if __name__ == "__main__":
    Utils.print_system_info()
