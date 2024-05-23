import os
from pyglet.image import load, SolidColorImagePattern

class Material:
    __filename_map__ = {
        "diffuse" : "diffuse.jpg",
        "ambient" : "ambient.jpg",
        "specular" : "specular.jpg",
        "roughness" : "roughness.jpg",
        "normal" : "normal.jpg",
    }
    
    def __init__(self, pathname = None):
        diffuse_path = os.path.join(pathname, self.__filename_map__["diffuse"])
        ambient_path = os.path.join(pathname, self.__filename_map__["ambient"])
        specular_path = os.path.join(pathname, self.__filename_map__["specular"])
        roughness_path = os.path.join(pathname, self.__filename_map__["roughness"])
        normal_path = os.path.join(pathname, self.__filename_map__["normal"])
        
        path_exists = pathname and os.path.exists(pathname)
        
        diffuse_exists = path_exists and os.path.exists(diffuse_path)
        ambient_exists = path_exists and os.path.exists(ambient_path)
        specular_exists = path_exists and os.path.exists(specular_path)
        roughness_exists = path_exists and os.path.exists(roughness_path)
        normal_exists = path_exists and os.path.exists(normal_path)
        
        diffuse_default = (int(0.5 * 255), int(0.5 * 255), int(0.5 * 255), 1)
        ambient_default = (int(0.1 * 255), int(0.1 * 255), int(0.1 * 255), 1)
        specular_default = (int(0.5 * 255), int(0.5 * 255), int(0.5 * 255), 1)
        roughness_default = (int(0.5 * 255), int(0.5 * 255), int(0.5 * 255), 1)
        normal_default = (int(0.8 * 255), int(0.8 * 255), int(0.8 * 255), 1)
        
        if diffuse_exists:
            self.diffuse = load(diffuse_path).get_texture()
        else:
            self.diffuse = SolidColorImagePattern(diffuse_default).create_image(1,1).get_texture()
            
        if ambient_exists:
            self.ambient = load(ambient_path).get_texture()
        else:
            self.ambient = SolidColorImagePattern(ambient_default).create_image(1,1).get_texture()
            
        if specular_exists:
            self.specular = load(specular_path).get_texture()
        else:
            self.specular = SolidColorImagePattern(specular_default).create_image(1,1).get_texture()
            
        if roughness_exists:
            self.roughness = load(roughness_path).get_texture()
        else:
            self.roughness = SolidColorImagePattern(roughness_default).create_image(1,1).get_texture()
            
        if normal_exists:
            self.normal = load(normal_path).get_texture()
        else:
            self.normal = SolidColorImagePattern(normal_default).create_image(1,1).get_texture()