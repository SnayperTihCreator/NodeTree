from dataclasses import dataclass, field

import pygame as pg

from Nodes.handlers import NameSpace, EventLoopHandler, GameLoopHandler
from Nodes.scenes.base import BaseScene
from Nodes.scenes.switcher import SwitcherScenes


@dataclass
class NameSpaceScene(NameSpace):
    scene: BaseScene
    switcher: SwitcherScenes = field(repr=False)

    def switchToSceneName(self, name):
        self.switcher.switch(name)


class DefaultMetaScene:
    eventHandler = EventLoopHandler
    loopHandler = GameLoopHandler
    nameSpace = NameSpaceScene
    argsNameSpace = []
    colorBackground = pg.Color(0, 0, 0)


class Scene(BaseScene):
    class Meta(DefaultMetaScene): ...

    def __init__(self, switcher):
        super().__init__(switcher)
        self.switcher = switcher
        self.eventHandler: EventLoopHandler = self.Meta.eventHandler()
        self.loopHandler: GameLoopHandler = self.Meta.loopHandler()
        self.ns: NameSpaceScene = self.Meta.nameSpace(self, switcher, *self.Meta.argsNameSpace)

        self._has_set_out_draw = True

    def __event__(self, event):
        self.eventHandler.__event__(event, self.ns)

    def __update__(self):
        self.loopHandler.update(self.ns)

    def __preUpdate__(self, timeDelta, allTime):
        self.ns.timeDelta = timeDelta
        self.ns.allTime = allTime
        self.loopHandler.preUpdate(self.ns)

    def __initNameSpace__(self):
        self.loopHandler.initNameSpace(self.ns)
