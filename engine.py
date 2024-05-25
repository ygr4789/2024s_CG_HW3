import pyglet
import numpy as np

from render import RenderWindow
from geometry import *
from material import *
from light import *

from object3d import Object3D
from control import Control

from obj_parse import parse_obj


class Engine:
    def __init__(self, renderer: RenderWindow, controller: Control):
        self.renderer = renderer
        self.controller = controller
        renderer.fixed_update = self.fixed_update
        self.setup()

    def setup(self):
        # mesh_list = parse_obj("model/Daven/Daven.obj")
        mesh_list = parse_obj("model/Car/classic_car_2.obj")
        for mesh in mesh_list:
            obj = Object3D(mesh.geometry, mesh.material)
            self.renderer.add_object(obj)
        self.set_lights()

    def set_lights(self):
        pos_list = [
            Vec3(-0.818657, 2.72386, 2.09402, ),
            Vec3(-2.29035,2.57604, - 1.76613, ),
            Vec3(1.34966, 2.74968, 0.873614, ),
            Vec3(0.939111, 2.43263, 2.95849, ),
            Vec3(0.313981,7.45584, - 9.43901, ),
            Vec3(-5.2941,7.9253, - 12.1689, ),
            Vec3(-9.47955, 4.05675, 10.0578, ),
        ]
        color_list = [
            Vec3(1, 1, 1),
            Vec3(0.286389, 0.649389, 1.0),
            Vec3(1.0, 0.756669, 0.669573),
            Vec3(1.0, 1.0, 1.0),
            Vec3(1.0, 1.0, 1.0),
            Vec3(1.0, 1.0, 1.0),
            Vec3(0.477269, 0.587244, 1.0),
        ]
        power_list = [43.1969, 121.737, 121.737, 55, 255, 985.675, 1771.07]

        for pos, color, power in zip(pos_list, color_list, power_list):
            self.renderer.point_lights.append(PointLight(pos, color, power))

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
