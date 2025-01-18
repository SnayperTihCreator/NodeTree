import pygame as pg

from Nodes.screeeRenders.base import BaseScreenProvider, BaseManagerRender, RenderData


class OpenGlProvider(BaseScreenProvider):
    def __init__(self, size, flags=0):
        super().__init__(size, flags)

    def blitImage(self, surf, pos):
        pass

    def render(self):
        pass

    def renderBackground(self):
        pass

    def resizeRecalculate(self, size):
        pass


class ManagerRenderOpenGl(BaseManagerRender):
    def __init__(self, size, flags, bgColor, bgImage):
        pass

    def render(self):
        pass

    def renderBackground(self):
        pass