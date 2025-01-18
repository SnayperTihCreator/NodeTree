import time

import pygame as pg

from Nodes.scenes.base import BaseTree
from Nodes.scenes.switcher import SwitcherScenes
from Nodes.utils import ManagerAutoSize


class DefaultMetaTree:
    switcherScene = SwitcherScenes
    clock = pg.time.Clock
    fps = 60
    windowSize = pg.Vector2(600, 400)
    windowFlag = 0 #pg.OPENGL | pg.DOUBLEBUF #| pg.RESIZABLE


class MainTree(BaseTree):
    class Meta(DefaultMetaTree):
        ...

    def __init__(self):
        super().__init__()
        self.switcherScene = self.Meta.switcherScene()
        ManagerAutoSize().resize.connect(self.resized)
        self.switcherScene.app = self
        self.clock = self.Meta.clock()
        self.fps = self.Meta.fps

        self.screen = self.createMainWindow()
        self.display = pg.Surface(self.Meta.windowSize, pg.SRCALPHA)

    def createMainWindow(self):
        return pg.display.set_mode(self.Meta.windowSize, self.Meta.windowFlag)

    def resized(self, size):
        self.Meta.windowSize = size

    def run(self):
        self.switcherScene.run()
        itGetScene = self.switcherScene.getScene()
        start_time = time.time()
        while (scene := next(itGetScene)) is not None:
            timeDelta = self.clock.tick(self.fps) / 1000.0
            self.display.fill(scene.Meta.colorBackground)
            scene.__preUpdate__(timeDelta, time.time() - start_time)
            for e in pg.event.get():
                scene.__event__(e)
            scene.__update__()
            self.screen.blit(self.display, (0, 0))

            pg.display.flip()
