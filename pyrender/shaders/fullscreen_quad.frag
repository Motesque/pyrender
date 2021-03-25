#version 330 core

uniform sampler2D bg_image;
in vec2 texture_coord;
out vec4 frag_color;

void main() {
   vec4 bg_color = texture2D(bg_image, texture_coord);
   frag_color = vec4(bg_color.xyz, 1);
}