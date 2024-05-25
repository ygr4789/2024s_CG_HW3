import os

import pprint

from pyglet.util import asstr
from pyglet.math import Vec3

from geometry import *
from material import *

TEXTUER_PATH = "texture"

class Mesh:
    def __init__(self, name:str):
        self.name = name
        self.geometry = Geometry()
        self.material = None
        self.material_name = None

def find_file(directory, file_subpath):
    for dirpath, _, _ in os.walk(directory):
        relative_dirpath = os.path.relpath(dirpath, directory)
        potential_file_path = os.path.join(relative_dirpath, file_subpath)
        full_potential_file_path = os.path.join(directory, potential_file_path)
        if os.path.isfile(full_potential_file_path):
            return full_potential_file_path
    return None

def load_material_library(filename):
    file = open(filename, 'r')
    location = os.path.dirname(filename)

    name = None
    matlib = {}
    
    lines = [line for line in file] + ['newmtl EOF'] # save last material

    for line in lines:
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == 'newmtl':
            if name is not None:
                # save previous material
                matlib[name] = Material(**mat_args)
            
            # initialize
            name = values[1]
            mat_args = {}

        elif name is None:
            raise Exception(f'Expected "newmtl" in {filename}')

        try:
            if values[0] == 'Kd':
                mat_args["diffuse"] = list(map(float, values[1:]))
            elif values[0] == 'Ka':
                mat_args["ambient"] = list(map(float, values[1:]))
            elif values[0] == 'Ks':
                mat_args["specular"] = list(map(float, values[1:]))
            elif values[0] == 'Ke':
                mat_args["emission"] = list(map(float, values[1:]))
            elif values[0] == 'Ns':
                mat_args["roughness"] = [(2/(float(values[1])+2)) ** (1/4)] * 3 # convert shininess to roughness
            elif values[0] == 'd':
                mat_args["opacity"] = [float(values[1])] * 3
            elif values[0] == 'refl':
                mat_args["metallic"] = [float(values[1])] * 3
            elif values[0].startswith('map'):
                tex_path = find_file(location, values[-1])
                if tex_path:
                    if values[0] == 'map_Kd':
                        mat_args["diffuse"] = tex_path
                    elif values[0] == 'map_Ka':
                        mat_args["ambient"] = tex_path
                    elif values[0] == 'map_Ks':
                        pass
                        mat_args["specular"] = tex_path
                    elif values[0] == 'map_Ke':
                        mat_args["emission"] = tex_path
                    elif values[0] == 'map_Ns':
                        mat_args["roughness"] = tex_path
                    elif values[0] == 'map_d':
                        mat_args["opacity"] = tex_path
                    elif values[0] == 'map_refl' or values[0] == 'map_Refl':
                        mat_args["metallic"] = tex_path
                    elif values[0] == 'map_bump' or values[0] == 'map_Bump':
                        mat_args["bump"] = tex_path

        except BaseException as ex:
            raise Exception('Parsing error in {0}.'.format((filename, ex)))

    file.close()

    return matlib


def parse_obj(filename, file=None):
    materials = {}
    mesh_list: list[Mesh] = []
    
    location = os.path.dirname(filename)
    
    default_material = Material()
    material = None
    mesh = None
    
    try:
        if file is None:
            with open(filename, 'r') as f:
                file_contents = f.read()
        else:
            file_contents = asstr(file.read())
    except (UnicodeDecodeError, OSError):
        raise Exception("ModelDecodeException")

    vertices = [[0., 0., 0.]]
    normals = [[0., 0., 0.]]
    uvs = [[0., 0.]]

    for line in file_contents.splitlines():

        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == 'v':
            vertices.append(list(map(float, values[1:4])))
        elif values[0] == 'vn':
            normals.append(list(map(float, values[1:4])))
        elif values[0] == 'vt':
            uvs.append(list(map(float, values[1:3])))
            
        elif values[0] == 'mtllib':
            material_abspath = os.path.join(location, values[1])
            materials = load_material_library(filename=material_abspath)  
            
        elif values[0] in ('usemtl', 'usemat'):
            material = materials.get(values[1])
            if mesh is not None:
                mesh.material = material
                mesh.material_name = values[1]
                
        elif values[0] == 'g':
            mesh = Mesh(name=values[1])
            mesh.material = default_material
            mesh_list.append(mesh)
            
        elif values[0] == 'f':
            if mesh is None:
                mesh = Mesh(name='')
                mesh_list.append(mesh)
            if material is None:
                material = default_material
            if mesh.material is None:
                mesh.material = material
            
            # For fan triangulation, remember first and latest vertices
            n2 = None
            t2 = None
            v2 = None

            for i, v in enumerate(values[1:]):
                v_i, t_i, n_i = (list(map(int, [j or 0 for j in v.split('/')])) + [0, 0])[:3]
                if v_i < 0:
                    v_i += len(vertices) - 1
                if t_i < 0:
                    t_i += len(uvs) - 1
                if n_i < 0:
                    n_i += len(normals) - 1

                if i == 0:
                    n0 = normals[n_i]
                    t0 = uvs[t_i]
                    v0 = vertices[v_i]
                    
                n1 = n2
                t1 = t2
                v1 = v2
                
                n2 = normals[n_i]
                t2 = uvs[t_i]
                v2 = vertices[v_i]

                if i >= 2:
                    # Triangulate
                    mesh.geometry.normals += n0 + n1 + n2
                    mesh.geometry.uvs += t0 + t1 + t2
                    mesh.geometry.vertices += v0 + v1 + v2
                    
                    p0v = Vec3(*v0)
                    p1v = Vec3(*v1)
                    p2v = Vec3(*v2)
                    p01v = p1v - p0v
                    p02v = p2v - p0v
                    
                    u01 = t1[0] - t0[0]
                    u02 = t2[0] - t0[0]
                    v01 = t1[1] - t0[1]
                    v02 = t2[1] - t0[1]
                    
                    tv = (p01v * v02 - p02v * v01).normalize()
                    bv = (-p01v * u02 + p02v * u01).normalize()
                    
                    mesh.geometry.t += [*tv.xyz] * 3
                    mesh.geometry.b += [*bv.xyz] * 3

    return mesh_list