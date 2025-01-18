import abc
import pygame as pg


class BaseObject(abc.ABC):
    pass


class Transform2D(BaseObject):
    def __init__(self, rect:pg.Rect, rotated=0, flip_h=False, flip_w=False):
        self.rect = rect
        self.rotated = rotated
        self.flip_h = flip_h
        self.flip_w = flip_w

        self._source_size = pg.Vector2(rect.size)

    @property
    def scale(self):
        currentSize = pg.Vector2(self.rect.size)
        return currentSize.elementwise()/self._source_size

    @scale.setter
    def scale(self, value):
        self.rect.scale_by_ip(value)

