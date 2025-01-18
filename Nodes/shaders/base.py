
DEFAULT_VERTEX_SHADER = """
#version 330 core

layout (location = 0) in vec3 vertexPos;
layout (location = 1) in vec2 vertexTexCoord;

out vec2 uvs;

void main()
{
    uvs = vertexTexCoord;
    gl_Position = vec4(vertexPos, 1.0);
}
"""

DEFAULT_FRAGMENT_SHADER = """
#version 330 core

in vec3 fragmentColor;
in vec2 uvs;

out vec4 color;

uniform sampler2D imageTexture;

void main() {
    color = texture(imageTexture, uvs);
}
"""