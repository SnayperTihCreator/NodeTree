import pygame as pg

from Nodes.shaders.base import DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER
from Nodes.shaders.shader import Shader


class DefaultScreenShader(Shader):
    def __init__(self, screen: pg.Surface) -> None:
        super().__init__(DEFAULT_VERTEX_SHADER, DEFAULT_FRAGMENT_SHADER, screen)

    def render(self, update_surface: bool = True)->None:
        super().render_direct(pg.Rect((0, 0), self.target_surface.get_size()),
                              update_surface, True)