import pyglet
import numpy as np

from render import RenderWindow
from geometry import *
from material import *

from pyglet.gui import WidgetBase
from pyglet.math import Vec4

from object_3d import Object3D
from object_line import ObjectLine
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
        
        
        self.grid_helper = ObjectLine(grid_lines(), Vec4(0.25,0.25,0.25,1))
        self.renderer.add_object(self.grid_helper)
        self.update_visibility()
        
    def update_visibility(self):
        ui = self.renderer.ui
        grid = ui.grid_active
        wireframe = ui.wireframe_active
        control = ui.control_active
        
        self.grid_helper.group.visible = grid
        
    def update_grid_helper(self):
        ui = self.renderer.ui
        size = ui.grid_size
        unit = ui.grid_unit
        
        self.grid_helper.update(grid_lines(size, unit))
        
    def fixed_update(self, dt):
        ui = self.renderer.ui
        self.controller.disabled = ui.focused
        
        queue = ui.command_queue
        while len(queue) > 0:
            cmd = queue.pop(0)
            try:
                if cmd == "change_mode":
                    pass
                elif cmd == "import":
                    pass
                elif cmd == "export":
                    pass
                elif cmd == "reset":
                    pass
                elif cmd == "update_curve":
                    pass
                elif cmd == "update_subdiv":
                    pass
                elif cmd == "update_grid":
                    self.update_grid_helper()
                elif cmd == "update_color":
                    pass
                elif cmd == "update_visibility":
                    self.update_visibility()
            except Exception as e:
                raise e
                ui.log(e)