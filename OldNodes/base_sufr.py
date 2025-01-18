import pygame as _pg
from collections import UserList
from OldNodes import MetaSkipData


class Image(_pg.Surface, metaclass=MetaSkipData):

    def __init__(self, surf, path=None):
        super().__init__(surf.get_size(), _pg.SRCALPHA)
        self.path_img = path
        self.blit(surf, (0, 0))

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.size}, alpha={self.get_alpha()})>"

    @classmethod
    def createFromPath(cls, path):
        img = _pg.image.load(path)
        return cls(img, path)

    def scale(self, size):
        suf = _pg.transform.scale(self, size)
        return Image(suf)


class ImageSeq(UserList):
    def __init__(self, *imgs):
        super().__init__(imgs)

    def scale(self, size):
        return [img.scale(size) for img in self]


class ColorRect(_pg.Surface):
    def __init__(self, color, size):
        super().__init__(size)
        clr = _pg.Color(color)
        self.fill(clr)
