import pathlib
import types
import typing
from dataclasses import dataclass, field

import pygame as pg
import taichi as ti

from Nodes.shaders_taichi.screen_rect import ScreenRect
from Nodes.shaders_taichi.texture import Texture


@dataclass
class InputFragment:
    imageTexture: ti.types.ndarray() = field(init=False)
    fragColor: ti.math.vec3 = field(default=ti.math.vec3(0))
    uv: ti.math.vec2 = field(default=ti.math.vec2(0))


@dataclass
class OutputFragment:
    color: ti.math.vec4 = field(default=ti.math.vec4(0))


@ti.data_oriented
class Locals(types.ModuleType):
    def __init__(self):
        super().__init__("locals")

    @ti.func
    def texture(self, imgTexture, uv) -> ti.math.vec4:
        rsn = ti.math.vec2(imgTexture.shape)
        pos = uv * rsn
        return ti.math.vec4(imgTexture[pos.x, rsn.y - pos.y], 1.0)


local = Locals()


@ti.data_oriented
class BaseShader:
    def __init__(self, surface):
        self.texture = Texture(surface)
        self.inData = InputFragment()
        self.outData = OutputFragment()

        self._rsn = ti.math.vec2(0)
        self._result_data = None

        self.calculate()

    def calculate(self):
        self._rsn = ti.math.vec2(self.texture.texture_field.shape)
        self.inData.imageTexture = self.texture.getImageTexture()

    def render(self):
        self._result_data = self.texture.createEmptyField()
        self.__render__(self.texture.texture_field)
        return self.texture.__render__(self._result_data.to_numpy())

    @staticmethod
    @ti.func
    def _getFragColor(x, y):
        return ti.math.vec3(0)  #self.texture.texture_field[x, self._rsn.y - y]

    @ti.func
    def _setDataOutFragment(self, x, y, color):
        self._result_data[x, self._rsn.y - y] = ti.math.clamp(color, 0.0, 1.0)

    @ti.kernel
    def __render__(self, tex_field: ti.types.ndarray()):
        for frag_coord in ti.grouped(tex_field):
            color = self.fragment(tex_field, frag_coord / self._rsn, self._getFragColor(frag_coord.x, frag_coord.y))
            self._setDataOutFragment(frag_coord.x, frag_coord.y, color)


    @ti.func
    def fragment(self, imageTexture, uv, fragColor):
        return local.texture(imageTexture, uv)
