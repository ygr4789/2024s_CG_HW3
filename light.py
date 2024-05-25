from pyglet.math import Vec3
from pyglet.graphics.shader import ShaderProgram

class DirLight:
    def __init__(self, dir: Vec3 = Vec3(10, 10, 10), color:Vec3 = Vec3(1, 1, 1), power: float = 1):
        self.dir = dir
        self.color = color
        self.power = power
    def assign_to(self, sp: ShaderProgram, index: int):
        sp[f'dir_lights[{index}].dir'] = self.dir
        sp[f'dir_lights[{index}].color'] = self.color
        sp[f'dir_lights[{index}].power'] = self.power
        
        
class PointLight:
    def __init__(self, pos: Vec3 = Vec3(10, 10, 10), color:Vec3 = Vec3(1, 1, 1), power: float = 1):
        self.pos = pos
        self.color = color
        self.power = power
    def assign_to(self, sp: ShaderProgram, index: int):
        sp[f'point_lights[{index}].pos'] = self.pos
        sp[f'point_lights[{index}].color'] = self.color
        sp[f'point_lights[{index}].power'] = self.power