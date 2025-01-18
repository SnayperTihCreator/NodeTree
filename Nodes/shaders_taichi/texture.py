import os
import typing

import pygame as pg
import taichi as ti
import numpy as np


@ti.data_oriented
class Texture:
    def __init__(self, image: pg.Surface):
        self.surface: pg.Surface = image.copy()
        self.texture_array = pg.surfarray.array3d(image).astype(np.float32) / 255
        self.texture_field = ti.Vector.ndarray(3, ti.float32, image.get_size())
        self.texture_field.from_numpy(self.texture_array)

    def __render__(self, source):
        result = pg.Surface(self.surface.get_size(), pg.SRCALPHA)
        pg.surfarray.blit_array(result, source)
        return result

    def getImageTexture(self):
        return self.texture_field

    def createEmptyField(self):
        return ti.Vector.ndarray(3, ti.float32, self.surface.get_size())
