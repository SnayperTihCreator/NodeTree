import enum
from dataclasses import dataclass

import pygame as pg
from threading import Thread
from time import sleep


class MetaSingtoon(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class MetaSkipData(type):
    def __call__(cls, *args, **kwargs):
        if len(args) == 1 and type(args[0]) is cls:
            return args[0]
        return super().__call__(*args, **kwargs)


class ManagerNode:
    _sender_last = None

    def __init__(self):
        self.groups = []
        self.style = Style()
        self.handsurf = None

    def initStyle(self, path):
        self.style.path_style = path
        self.style.initForm()

    def add_group(self, group):
        self.groups.append(group)

    def updateAll(self, **kwargs):
        [grp.update(**kwargs) for grp in self.groups]

    def updateVisible(self, **kwargs):
        for grp in self.groups:
            if grp.visible:
                grp.update(**kwargs)

    def sender(self):
        return self._sender_last

    def render(self, element):
        self.handsurf = pg.Surface(element.rect.size, pg.SRCALPHA)
        opt = element.delegate.opt(self.handsurf, self.style)
        return element.delegate.render(opt)


@dataclass
class StyleOption:
    rect: pg.Rect
    image: pg.Surface
    screen: pg.Surface

    def copy(self):
        return StyleOption(self.rect.copy(), self.image.copy(), self.screen)


class Style(metaclass=MetaSingtoon):

    def __init__(self):
        self.path_style = None
        self.__default_style = {

        }
        self.element_style = {}

    def initForm(self):
        pass

    def getStyleOption(self, obj):
        pass


class Signal:
    class FlagConnect(enum.IntEnum):
        AutoConnect = 1
        OneShotConnect = 2

    def __init__(self):
        self._handlers = {}
        self._instance = None

    def __get__(self, instance, owner):
        self._handlers.setdefault(instance, [])
        self._instance = instance
        return self

    def connect(self, handler, flags=1):
        self._handlers[self._instance].append((handler, flags))

    def hasConnect(self, handler):
        return bool((hand, _) for hand, _ in self._handlers[self._instance] if hand == handler)

    def disconnect(self, handler, strict=False):
        if self.hasConnect(handler) and strict:
            ValueError("Not connect handler")
        for i, (hand, _) in enumerate(self._handlers[self._instance]):
            if hand == handler:
                self._handlers[self._instance].pop(i)
                return True
        return False

    def emit(self, *args, **kwargs):
        ManagerNode._sender_last = self._instance
        for hand, flags in self._handlers[self._instance]:
            hand(*args, **kwargs)
            if flags & self.FlagConnect.OneShotConnect:
                self.disconnect(hand)
        ManagerNode._sender_last = None


class NodeTypeEvent(enum.IntEnum):
    SCENAENTER = pg.event.custom_type()
    SCENAEXIT = pg.event.custom_type()
    MOUSEBTNDOWN = pg.event.custom_type()
    MOUSEBTNUP = pg.event.custom_type()
    MOUSEWHEEL = pg.event.custom_type()
    MOUSEMOTION = pg.event.custom_type()


class ManagerThread(metaclass=MetaSingtoon):
    class Timer(Thread):
        timeout = Signal()

        def __init__(self, n, sec, oneLoop=False):
            super().__init__(name=f"Timer-{n}", daemon=True)
            self.time_stop = sec
            self.oneLoop = oneLoop
            self.is_stop = False

        def run(self):
            clock = self.tick()
            while True:
                try:
                    if self.is_stop:
                        self.timeout.emit()
                        break
                    next(clock)
                    sleep(1)
                except StopIteration:
                    self.timeout.emit()
                    clock = self.tick()
                    if self.oneLoop:
                        break

        def tick(self):
            ost = self.time_stop
            ost -= 1
            yield ost

        def stop(self):
            self.is_stop = True

    def __init__(self):
        self.threadsGame = []
        self.nPlugin = 0
        self.nTimer = 0

    def createThreadGame(self, name, target, *args, **kwargs):
        th = Thread(name=name, target=target, args=args, kwargs=kwargs, daemon=True)
        self.threadsGame.append(th)
        return th

    def createThreadPlugin(self, target, *args, **kwargs):
        self.nPlugin += 1
        return Thread(name=f"Plugin-{self.nPlugin}", target=target, args=args, kwargs=kwargs, daemon=True)

    def createTimer(self, sec, oneLoop=False):
        self.nTimer += 1
        return self.Timer(self.nTimer, sec, oneLoop)

    def runGameThread(self):
        [th.start() for th in self.threadsGame]


class UnionRect(pg.Rect):
    def __init__(self, *rects):
        super().__init__()
        self.unionall_ip(rects)
