import pathlib
import typing

import moderngl
import pygame as pg

from Nodes.shaders.screen_rect import ScreenRect
from Nodes.shaders.texture import Texture


class Shader:
    @staticmethod
    def create_vert_frag_shader(vertex, fragment, ctx: moderngl.Context):
        vertexPath = pathlib.Path(vertex)
        fragmentPath = pathlib.Path(fragment)

        vertexSource = vertexPath.read_text("utf-8") if vertexPath.exists() else vertex
        fragmentSource = fragmentPath.read_text("utf-8") if fragmentPath.exists() else fragment

        shader = ctx.program(
            vertex_shader=vertexSource,
            fragment_shader=fragmentSource
        )
        return shader

    def __init__(self, vertexPath, fragmentPath, surface: pg.Surface):

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = self.ctx.SRC_ALPHA, self.ctx.ONE_MINUS_SRC_ALPHA

        self._vertexPath = vertexPath
        self._fragmentPath = fragmentPath

        self.target_surface = surface

        self.shader_data = {}
        self.shader = Shader.create_vert_frag_shader(vertexPath, fragmentPath, self.ctx)
        self.render_rect = ScreenRect(surface.get_size(), surface.get_size(), (0, 0), self.ctx, self.shader)

        self.screen_texture = Texture(pg.Surface(surface.get_size()), self.ctx)
        self.framebuffer = self.ctx.simple_framebuffer(size=self.target_surface.get_size(), components=4)
        self.scope = self.ctx.scope(self.framebuffer)
        self.window_size = pg.display.get_surface().get_size()

    def updateSurface(self, surface: pg.Surface):
        self.target_surface = surface

        self.render_rect = ScreenRect(surface.get_size(), surface.get_size(), (0, 0), self.ctx, self.shader)
        self.screen_texture = Texture(pg.Surface(surface.get_size()), self.ctx)
        self.framebuffer = self.ctx.simple_framebuffer(size=self.target_surface.get_size(), components=4)
        self.scope = self.ctx.scope(self.framebuffer)

    def updateWindowSize(self):
        self.window_size = pg.display.get_surface().get_size()

    def clear(self, color: typing.Union[pg.Color, typing.Tuple[int, int, int, int]]):
        self.target_surface.fill(color)
        self.ctx.clear(color=(color[0] / 255, color[1] / 255, color[2] / 255, 1.0))

    def uniform(self, name: str, data: typing.Any):
        self.shader[name] = data

    def render(self, update_surface: bool = True) -> pg.Surface:
        if update_surface:
            self.screen_texture.update(self.target_surface)
        self.screen_texture.use()

        with self.scope:
            self.framebuffer.use()
            self.render_rect.vao.render()
            surf = pg.image.frombuffer(self.framebuffer.read(), self.target_surface.get_size(), "RGB")
        return pg.transform.flip(surf, False, True)

    def render_direct(self, rect: pg.Rect, update_surface: bool = True, autoscale: bool = False):
        if autoscale:
            size = (self.target_surface.get_width(), self.target_surface.get_height())
        else:
            size = self.window_size

        rect = ScreenRect.pygame_rect_to_screen_rect(rect, size)

        # self.__upload_uniforms()
        self.render_rect = ScreenRect((rect.w, rect.h), size, (rect.x, rect.y), self.ctx, self.shader)

        if update_surface:
            self.screen_texture.update(self.target_surface)

        self.screen_texture.use()
        self.render_rect.vao.render()
