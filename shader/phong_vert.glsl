#version 330
in vec3 vertices;
in vec3 normals;
in vec2 uvs;

in vec3 texvec_t;
in vec3 texvec_b;

out vec2 tex_coord;
out vec3 normal;
out vec3 pos;
out vec3 t;
out vec3 b;

uniform mat4 model;
uniform mat4 view_proj;

void main()
{
    vec4 world_pos = model * vec4(vertices, 1.0f);
    gl_Position = view_proj * world_pos; // local->world->vp
    
    pos = world_pos.xyz;
    normal = (model * vec4(normals, 0.0f)).xyz;
    
    tex_coord = uvs;
    
    t = texvec_t;
    b = texvec_b;
}