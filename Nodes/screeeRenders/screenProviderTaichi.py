import pygame as pg

from Nodes.screeeRenders.base import BaseScreenProvider, BaseManagerRender, RenderData


class TaichiProvider(BaseScreenProvider):

    def __init__(self, size, rd, flags=0):
        super().__init__(size, flags)
        flags |= pg.RESIZABLE
        self._screen = pg.display.set_mode(size, flags)
        self._display = pg.Surface(size, pg.SRCALPHA)
        self._renderData: RenderData = rd
        self._renderData.recalculate(size)
        self.currentSize = size

    def blitImage(self, surf, pos):
        self._display.blit(surf, pos)

    def render(self):
        src = pg.transform.smoothscale(self._display, self.currentSize)
        self._screen.blit(src, (0, 0))

    def renderBackground(self):
        if self._renderData.bgImage is None:
            self._display.fill(self._renderData.bgColor)
        else:
            self._display.blit(self._renderData.bgImage, (0, 0))

    def resizeRecalculate(self, size):
        self.currentSize = size
        self._renderData.recalculate(size)


class ManagerRenderTaichi(BaseManagerRender):
    def __init__(self, size, flags=0, bgColor=pg.Color("black"), bgImage=None):
        rd = RenderData(bgColor, bgImage)
        self.provider = TaichiProvider(size, rd, flags)

    def render(self):
        self.provider.render()

    def renderBackground(self):
        self.provider.renderBackground()
