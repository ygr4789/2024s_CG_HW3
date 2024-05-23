from pyglet.util import asstr
from pyglet.math import Vec2, Vec3

from .geom import Geometry

def parse_obj_file(filename, file=None):
    geo = Geometry()
    
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
    geo.normals = []
    geo.uvs = []
    geo.n = []
    geo.b = []
    geo.t = []

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
        elif values[0] == 'f':
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
                    geo.normals += n0 + n1 + n2
                    geo.uvs += t0 + t1 + t2
                    geo.vertices += v0 + v1 + v2
                    
                    p0v = Vec3(*v0)
                    p1v = Vec3(*v1)
                    p2v = Vec3(*v2)
                    p01v = p1v - p0v
                    p02v = p2v - p0v
                    
                    u01 = t1[0] - t0[0]
                    u02 = t2[0] - t0[0]
                    v01 = t1[1] - t0[1]
                    v02 = t2[1] - t0[1]
                    
                    tv = (p01v * v02 - p02v * u02).normalize()
                    bv = (-p01v * v01 + p02v * u01).normalize()
                    tv = Vec3()
                    bv = Vec3()
                    
                    geo.t += [*tv.xyz] * 3
                    geo.b += [*bv.xyz] * 3

    return geo