import pyglet
from pyglet.math import Mat4, Vec3

from render import RenderWindow
from geometry.geom import *
from control import Control

from object3d import Object3D
from engine import Engine

if __name__ == '__main__':
    width = 1280
    height = 720

    # Render window.
    renderer = RenderWindow(width, height, "Shading", resizable = True)   
    renderer.set_location(200, 200)

    # Keyboard/Mouse control. Not implemented yet.
    controller = Control(renderer)
    engine = Engine(renderer, controller)

    #draw shapes
    renderer.run()
