#version 330

// in-out

in vec2 tex_coord;
in vec3 pos;
in vec3 normal;
in vec3 b;
in vec3 t;

out vec4 out_color;

// textures

uniform sampler2D texture0;
uniform sampler2D texture1;
uniform sampler2D texture2;
uniform sampler2D texture3;
uniform sampler2D texture4;
uniform sampler2D texture5;
uniform sampler2D texture6;


// global vairables

vec3 k_a;
vec3 k_s;
vec3 k_d;
vec3 n;
float shininess;
float opacity;
float oplus;

vec3 k_m;
float refl;

// lights

struct dir_light {
    vec3 dir;
    vec3 color;
    float power;
};

struct point_light {
    vec3 pos;
    vec3 color;
    float power;
};

vec3 calc_dir_light(dir_light light);
vec3 calc_point_light(point_light light);

#define NR_DIR_LIGHTS 4
#define NR_POINT_LIGHTS 10

uniform float ambient_power;
uniform vec3 cam_eye;
uniform dir_light dir_lights[NR_DIR_LIGHTS];
uniform point_light point_lights[NR_POINT_LIGHTS];

float light_coeff = 40.0;

void main() {
    vec4 tex0_v = texture2D(texture0, tex_coord); // diffuse
    vec4 tex1_v = texture2D(texture1, tex_coord); // ambient
    vec4 tex2_v = texture2D(texture2, tex_coord); // normal
    vec4 tex3_v = texture2D(texture3, tex_coord); // roughness
    vec4 tex4_v = texture2D(texture4, tex_coord); // specular
    vec4 tex5_v = texture2D(texture5, tex_coord); // opacity
    vec4 tex6_v = texture2D(texture6, tex_coord); // metallic

    k_a = tex1_v.rgb;
    k_s = tex4_v.rgb;
    k_d = tex0_v.rgb;
    opacity = tex5_v.r;
    
    float roughness = tex3_v.r + 0.0001;
    float alpha = pow(roughness, 2);
    k_s /= (30 * pow(alpha, 2)); // custom roughness->specular conv
    shininess = 2 / pow(alpha, 2) - 2; // custom roughness->shininess conv

    n = normalize(normal);
    mat3 tbn = mat3(t, b, n);
    vec3 tbn_coord = tex2_v.rgb * 2 - 1;
    n = normalize(tbn * tbn_coord);
    
    // pseudo-bsdf implementation
    refl = tex6_v.r;
    k_m = refl * k_d;
    k_d *= (1 - refl);

    vec3 ambient = ambient_power * k_a;
    vec3 light = ambient;
    
    for(int i=0; i<NR_DIR_LIGHTS; i++)
        light += calc_dir_light(dir_lights[i]);
    for(int i=0; i<NR_POINT_LIGHTS; i++)
        light += calc_point_light(point_lights[i]);
    
    out_color = vec4(light, opacity + oplus / 2);
}

vec3 calc_dir_light(dir_light light) {
    
    vec3 pos_to_light = light.dir;
    vec3 pos_to_eye = cam_eye - pos;
    vec3 pos_to_light_dir = normalize(pos_to_light);
    vec3 pos_to_eye_dir = normalize(pos_to_eye);

    vec3 half_vec = normalize(pos_to_eye_dir + pos_to_light_dir);
    float glare = max(0.0, dot(n, half_vec));
    
    vec3 light_intensity = light.color * (light.power / light_coeff);

    vec3 diffuse = light_intensity * k_d * max(dot(n, pos_to_light_dir), 0.0);
    vec3 specular = light_intensity * k_s * pow(glare, shininess);
    vec3 reflect = light_intensity * k_m * pow(glare, 6);
    oplus += specular.x;
    
    return diffuse + specular + reflect;
}

vec3 calc_point_light(point_light light) {
    vec3 pos_to_light = light.pos - pos;
    vec3 pos_to_eye = cam_eye - pos;
    vec3 pos_to_light_dir = normalize(pos_to_light);
    vec3 pos_to_eye_dir = normalize(pos_to_eye);

    vec3 half_vec = normalize(pos_to_eye_dir + pos_to_light_dir);
    float glare = max(0.0, dot(n, half_vec));

    float dist_sq = pow(length(pos_to_light), 2);
    vec3 light_intensity = light.color * (light.power / light_coeff) / dist_sq;
    
    vec3 diffuse = light_intensity * k_d * max(dot(n, pos_to_light_dir), 0.0);
    vec3 specular = light_intensity * k_s * pow(glare, shininess);
    vec3 reflect = light_intensity * k_m * pow(glare, 6);
    oplus += specular.x;
    
    return diffuse + specular + reflect;
}