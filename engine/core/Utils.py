# fetched from https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021/blob/6f32e6b3537915cc15e4f3b6e3356a4e15bebb1c/py3d/core/utils.py

import OpenGL.GL as GL

from collections import namedtuple


class Utils:
    @staticmethod
    def get_system_info():
        vendor = GL.glGetString(GL.GL_VENDOR).decode('utf-8')
        renderer = GL.glGetString(GL.GL_RENDERER).decode('utf-8')
        opengl = GL.glGetString(GL.GL_VERSION).decode('utf-8')
        glsl = GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode('utf-8')
        Result = namedtuple('SystemInfo', ['vendor', 'renderer', 'opengl', 'glsl'])
        return Result(vendor, renderer, opengl, glsl)

    @staticmethod
    def print_system_info():
        info = Utils.get_system_info()
        result = ''.join(['Vendor: ', info.vendor, '\n',
                          'Renderer: ', info.renderer, '\n',
                          'OpenGL version supported: ', info.opengl, '\n',
                          'GLSL version supported: ', info.glsl])
        print(result)

if __name__ == "__main__":
    Utils.print_system_info()