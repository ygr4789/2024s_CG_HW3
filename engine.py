import pyglet
import numpy as np

from render import RenderWindow
from geometry import *
from material import *

from pyglet.gui import WidgetBase
from pyglet.math import Vec4

from object3d import Object3D
from control import Control

from pyglet.model import Model


class Engine:
    def __init__(self, renderer: RenderWindow, controller: Control):
        self.renderer = renderer
        self.controller = controller
        renderer.fixed_update = self.fixed_update
        self.setup()
        
    def setup(self):
        geo = parse_obj_file("model/Free_rock/mesh.obj")
        mat = Material("model/Free_rock/texture")
        
        obj = Object3D(geo, mat)
        self.renderer.add_object(obj)
        
    def update_visibility(self):
        ui = self.renderer.ui
        
    def fixed_update(self, dt):
        ui = self.renderer.ui
        self.controller.disabled = ui.focused
        
        queue = ui.command_queue
        
        while len(queue) > 0:
            cmd = queue.pop(0)
            try:
                if cmd == "invalid":
                    pass
            except Exception as e:
                raise e
                ui.log(e)