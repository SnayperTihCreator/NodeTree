import abc
from dataclasses import dataclass, field

import pygame as pg


class BaseScreenProvider(abc.ABC):
    def __init__(self, size, flags): ...

    @abc.abstractmethod
    def blitImage(self, surf, pos): ...

    @abc.abstractmethod
    def render(self): ...

    @abc.abstractmethod
    def renderBackground(self): ...

    @abc.abstractmethod
    def resizeRecalculate(self, size): ...


class BaseManagerRender(abc.ABC):
    @abc.abstractmethod
    def __init__(self, size, flags, bgColor, bgImage): ...

    @abc.abstractmethod
    def render(self): ...

    @abc.abstractmethod
    def renderBackground(self): ...


@dataclass
class RenderData:
    bgColor: pg.Color = field(default=pg.Color(0x000000))
    bgImage: pg.Surface = field(default=None)

    def recalculate(self, size):
        if self.bgImage is not None:
            self.bgImage = pg.transform.smoothscale(self.bgImage, size)
