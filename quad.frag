#version 460 core

layout (location = 0) out vec4 f_fragColor;

in VS_OUT
{
	vec2 texCoord;
} fs_in;

uniform sampler2D u_tex;

void main()
{
	f_fragColor = texture(u_tex, fs_in.texCoord);
	//f_fragColor = vec4(fs_in.texCoord, 0, 1);
}