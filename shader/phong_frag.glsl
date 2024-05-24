#version 330
in vec2 tex_coord;
in vec3 pos;
in vec3 normal;
in vec3 b;
in vec3 t;

out vec4 out_color;

uniform sampler2D texture0;
uniform sampler2D texture1;
uniform sampler2D texture2;
uniform sampler2D texture3;
uniform sampler2D texture4;

uniform vec3 lpos;
uniform vec3 cam_eye;

float I_a = 0.2;
float I_l = 1.0;

struct dir_light {
    vec3 dir;
    vec3 color;
    float I0;
};

struct point_light {
    vec3 pos;
    vec3 color;
    float I0;
};

vec3 calc_dir_light(dir_light light, vec3 normal, vec3 viewDir);
vec3 calc_point_light(point_light light, vec3 normal, vec3 fragPos, vec3 viewDir);

#define NR_DIR_LIGHTS 4
#define NR_POINT_LIGHTS 4

uniform dir_light dir_lights[NR_DIR_LIGHTS];
uniform point_light point_lights[NR_POINT_LIGHTS];

void main() {
    vec4 tex0_v = texture2D(texture0, tex_coord); // diffuse
    vec4 tex1_v = texture2D(texture1, tex_coord); // ambient
    vec4 tex2_v = texture2D(texture2, tex_coord); // normal
    vec4 tex3_v = texture2D(texture3, tex_coord); // roughness
    vec4 tex4_v = texture2D(texture4, tex_coord); // specular

    vec3 k_a = tex1_v.rgb;
    vec3 k_s = tex4_v.rgb;
    vec3 k_d = tex0_v.rgb;
    vec3 tbn_coord = tex2_v.rgb * 2 - 1;
    float alpha = tex0_v.a;
    float roughness = tex3_v.x;
    float shininess = 2 / pow(roughness, 4) - 2;

    vec3 n = normalize(normal);
    mat3 tbn = mat3(t, b, n);
    n = normalize(tbn * tbn_coord);

    vec3 pos_to_light = lpos - pos;
    vec3 pos_to_eye = cam_eye - pos;
    vec3 pos_to_light_dir = normalize(pos_to_light);
    vec3 pos_to_eye_dir = normalize(pos_to_eye);

    vec3 half_vec = normalize(pos_to_eye_dir + pos_to_light_dir);
    float glare = max(0.0, dot(n, half_vec));

    float dist_sq = pow(length(pos_to_light_dir), 2);
    vec3 ambient = I_a * k_a;
    vec3 diffuse = (I_l / dist_sq) * k_d * max(dot(n, pos_to_light_dir), 0.0);
    vec3 specular = (I_l / dist_sq) * k_s * pow(glare, shininess);

    out_color = vec4(ambient + diffuse + specular, alpha);
}