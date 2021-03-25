#version 330 core

uniform mat4 view_mat;

in vec3 position;
out vec2 texture_coord;

void main() {
   texture_coord = position.xy * vec2(0.5,0.5) + vec2(0.5,0.5); // derive tech coord from vertix position
   gl_Position = vec4((view_mat * vec4(position,1)).xy,0.0,1.0);
}