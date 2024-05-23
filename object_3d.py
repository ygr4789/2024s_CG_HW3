import ctypes

import pyglet
from pyglet.math import Mat4, Vec4
from pyglet.gl import *

import shader.shader as shader
from geometry import *
from material import *


class CustomGroup(pyglet.graphics.Group):
    __totGroup__ = 0
    """
    To draw multiple 3D shapes in Pyglet, you should make a group for an object.
    """

    def __init__(self):
        super().__init__(CustomGroup.__totGroup__)
        CustomGroup.__totGroup__ += 1
        """
        Create shader program for each shape
        """
        self.shader_program = shader.create_program(
            shader.vertex_source_phong, shader.fragment_source_phong
        )
        self.transform_mat = Mat4()
        self.vlist = None
        self.textures = None
        self.shader_program.use()
        
        u_image0Location = glGetUniformLocation(self.shader_program.id, ctypes.create_string_buffer("texture0".encode()))
        u_image1Location = glGetUniformLocation(self.shader_program.id, ctypes.create_string_buffer("texture1".encode()))
        u_image2Location = glGetUniformLocation(self.shader_program.id, ctypes.create_string_buffer("texture2".encode()))
        u_image3Location = glGetUniformLocation(self.shader_program.id, ctypes.create_string_buffer("texture3".encode()))
        u_image4Location = glGetUniformLocation(self.shader_program.id, ctypes.create_string_buffer("texture4".encode()))
        glUniform1i(u_image0Location, 0)
        glUniform1i(u_image1Location, 1)
        glUniform1i(u_image2Location, 2)
        glUniform1i(u_image3Location, 3)
        glUniform1i(u_image4Location, 4)
        
    def set_state(self):
        self.shader_program.use()
        model = self.transform_mat
        self.shader_program["model"] = model
        glDepthFunc(GL_LESS)

        if self.textures :
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(self.textures["diffuse"].target, self.textures["diffuse"].id)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(self.textures["ambient"].target, self.textures["ambient"].id)
            glActiveTexture(GL_TEXTURE2)
            glBindTexture(self.textures["normal"].target, self.textures["normal"].id)
            glActiveTexture(GL_TEXTURE3)
            glBindTexture(self.textures["roughness"].target, self.textures["roughness"].id)
            glActiveTexture(GL_TEXTURE4)
            glBindTexture(self.textures["specular"].target, self.textures["specular"].id)

    def unset_state(self):
        self.shader_program.stop()

    def __eq__(self, other):
        return (
            self.__class__ is other.__class__
            and self.order == other.order
            and self.parent == other.parent
        )

    def __hash__(self):
        return hash((self.order))
    
    
class Object3D:
    def __init__(
        self,
        geometry: Geometry,
        material: Material,
    ):
        self.group = CustomGroup()
        self.material = material
        self.geometry = geometry
        self.parent: Object3D = None
        self.children: list[Object3D] = []
        self.translate_mat: Mat4 = Mat4()
        self.rotation_mat: Mat4 = Mat4()

    def set_batch(self, batch: pyglet.graphics.Batch):
        glLineWidth(10)
        count = len(self.geometry.vertices) // 3
        args = {
            "count": count,
            "mode": GL_TRIANGLES,
            "batch": batch,
            "group": self.group,
            "vertices": ("f", self.geometry.vertices),
            "normals" : ("f", self.geometry.normals),
            "uvs" : ("f", self.geometry.uvs),
            "texvec_t" : ("f", self.geometry.t),
            "texvec_b" : ("f", self.geometry.b),
        }
        self.group.vlist = self.group.shader_program.vertex_list(**args)
        
        self.group.textures = {
            "ambient" : self.material.ambient,
            "diffuse" : self.material.diffuse,
            "normal" : self.material.normal,
            "roughness" : self.material.roughness,
            "specular" : self.material.specular,
        }

    def calc_transform_mat(self):
        parent_transform_mat = Mat4()
        if self.parent is not None:
            parent_transform_mat = self.parent.group.transform_mat

        self.group.transform_mat = (
            parent_transform_mat @ self.translate_mat @ self.rotation_mat
        )
        for child in self.children:
            child.calc_transform_mat()
