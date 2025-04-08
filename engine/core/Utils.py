# fetched from https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021/blob/6f32e6b3537915cc15e4f3b6e3356a4e15bebb1c/py3d/core/utils.py

import pyglet
from collections import namedtuple


class Utils:
    @staticmethod
    def get_system_info() -> namedtuple:
        """
        Get a named tuple of various system info
        """
        vendor = pyglet.gl.gl_info.get_vendor()
        renderer = pyglet.gl.gl_info.get_renderer()
        opengl = pyglet.gl.gl_info.get_version_string()
        Result = namedtuple("SystemInfo", ["vendor", "renderer", "opengl"])
        return Result(vendor, renderer, opengl)

    @staticmethod
    def print_system_info() -> None:
        """
        Print relevant system info
        """
        info = Utils.get_system_info()
        result = "".join(
            [
                "Vendor: ",
                info.vendor,
                "\n",
                "Renderer: ",
                info.renderer,
                "\n",
                "OpenGL version supported: ",
                info.opengl,
            ]
        )
        print(result)

    @staticmethod
    def get_model_path(model: str) -> str:
        return f"assets/models/{model}/{model}.obj"


if __name__ == "__main__":
    Utils.print_system_info()
