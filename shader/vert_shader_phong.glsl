#version 330
in vec3 vertices;
in vec3 normals;
in vec2 uvs;

in vec3 texvec_t;
in vec3 texvec_b;

out vec2 texCoord;

out vec3 normal;
out vec3 pos_to_light;
out vec3 pos_to_eye;

out vec3 t;
out vec3 b;

// add a view-projection uniform and multiply it by the vertices

uniform vec3 dir_light;
uniform vec3 cam_eye;

uniform mat4 model;
uniform mat4 view_proj;

void main()
{
    vec4 world_pos = model * vec4(vertices, 1.0f);
    gl_Position = view_proj * world_pos; // local->world->vp
    
    pos_to_light = dir_light;
    pos_to_eye = cam_eye - world_pos.xyz;
    
    normal = (model * vec4(normals, 0.0f)).xyz;
    
    texCoord = uvs;
    
    t = texvec_t;
    b = texvec_b;
}