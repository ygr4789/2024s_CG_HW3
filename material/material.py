import os
from pyglet.image import load, SolidColorImagePattern


def load_texture(param):
    if isinstance(param, list):
        color = (*[int(c * 255) for c in param], 255)
        return SolidColorImagePattern(color).create_image(1, 1).get_texture()
    elif isinstance(param, str):
        return load(param).get_texture()
    else:
        raise Exception(f"{type(param)} is invalid material parameter type")


class Material:
    def __init__(
        self,
        diffuse=[0.0, 1.0, 0.0],
        ambient=[0.1, 0.1, 0.1],
        specular=[0.8, 0.8, 0.8],
        emission=[0.0, 0.0, 0.0],
        shininess=[0.02, 0.02, 0.02],
        opacity=[1.0, 1.0, 1.0],
        bump=[0.5, 0.5, 1.0],
    ):
        self.diffuse = load_texture(diffuse)
        self.ambient = load_texture(ambient)
        self.specular = load_texture(specular)
        self.roughness = load_texture(shininess)
        self.normal = load_texture(bump)
        self.opacity = load_texture(opacity)
