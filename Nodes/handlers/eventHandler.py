import pygame as pg

from Nodes.handlers.base import BaseHandler, NameSpace
from Nodes.utils import ManagerAutoSize


class EventLoopHandler(BaseHandler):
    def __init__(self):
        self.running = True
        self._lastHandlersEvent = []

    def registerHandlerEvent(self, handler):
        self._lastHandlersEvent.append(handler)

    def __event__(self, event: pg.event.Event, ns: NameSpace):
        self.allEvent(event, ns)
        match event.type:
            case pg.QUIT if self.closeEvent(event, ns):
                self.running = False
            case pg.KEYDOWN | pg.KEYUP:
                self.keyEvent(event, event.type == pg.KEYDOWN, ns)
            case pg.MOUSEBUTTONDOWN | pg.MOUSEBUTTONUP:
                self.mouseEvent(event, event.type == pg.MOUSEBUTTONDOWN, ns)
            case pg.MOUSEMOTION:
                self.mouseMotionEvent(event, ns)
            case pg.VIDEORESIZE:
                self.resizeWindowEvent(event, ns)
            case _:
                self.event(event, ns)
        [hand(event) for hand in self._lastHandlersEvent]

    def allEvent(self, event, ns):
        pass

    def event(self, event, ns):
        pass

    def closeEvent(self, event, ns):
        return True

    def keyEvent(self, event, pressed, ns):
        pass

    def mouseEvent(self, event, pressed, ns):
        pass

    def mouseMotionEvent(self, event, ns):
        pass

    def resizeWindowEvent(self, event, ns):
        ManagerAutoSize().resize.emit(event.size)