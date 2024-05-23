#version 330
in vec3 normal;
in vec2 texCoord;

in vec3 pos_to_light;
in vec3 pos_to_eye;

in vec3 b;
in vec3 t;

uniform sampler2D texture0;
uniform sampler2D texture1;
uniform sampler2D texture2;
uniform sampler2D texture3;
uniform sampler2D texture4;

out vec4 outColor;

void main()
{
    vec4 tex0_v = texture2D(texture0, texCoord); // diffuse
    vec4 tex1_v = texture2D(texture1, texCoord); // ambient
    vec4 tex2_v = texture2D(texture2, texCoord); // normal
    vec4 tex3_v = texture2D(texture3, texCoord); // roughness
    vec4 tex4_v = texture2D(texture4, texCoord); // specular
    
    float k_a = tex1_v.x;
    float k_s = tex4_v.x;
    float roughness = tex3_v.x;
    float shininess = 2/pow(roughness, 4) - 2;
    vec3 tbn_coord = tex2_v.xyz * 2 - 1;
    
    vec3 n = normalize(normal);
    mat3 mat_tbn = mat3(t, b, n);
    n = normalize(mat_tbn * tbn_coord);
    // n = n * 0.0000000001 + normalize(normal);
    
    vec3 pos_to_light_dir = normalize(pos_to_light);
    vec3 pos_to_eye_dir = normalize(pos_to_eye);
    vec3 half_ = normalize(pos_to_eye_dir + pos_to_light_dir);
    
    float ambient = k_a * 0.4;
    float diffuse = max(dot(n, pos_to_light_dir), 0.0f);
    
    float glare = dot(n, half_);
    float specular = 0.0f;
    if (glare > 0.0f) {
        specular = k_s * pow(dot(n, half_), shininess);
    }
    
    float light = ambient + diffuse + specular;
    
    outColor = tex0_v;
    outColor.xyz *= light;
}