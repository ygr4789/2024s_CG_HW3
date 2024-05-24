from pyglet.graphics.shader import Shader, ShaderProgram

# create vertex and fragment shader sources
vertex_source_phong = open('shader/phong_vert.glsl', 'r').read()
fragment_source_phong = open('shader/phong_frag.glsl', 'r').read()

def phong():
    return create_program(vertex_source_phong, fragment_source_phong)

def create_program(vs_source, fs_source):
    # compile the vertex and fragment sources to a shader program
    vert_shader = Shader(vs_source, 'vertex')
    frag_shader = Shader(fs_source, 'fragment')
    return ShaderProgram(vert_shader, frag_shader)