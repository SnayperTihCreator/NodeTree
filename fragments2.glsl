#version 330 core
in vec3 fragmentColor;
in vec2 uvs;

out vec4 color;

uniform sampler2D imageTexture;

uniform float time;

void main() {
    color = vec4(texture(imageTexture, uvs).rgb*cos(time), 1.0);
}

