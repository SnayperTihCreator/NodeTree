import enum

from Nodes.utils.base import AManager


class ManagerSignal(AManager):
    def __init__(self):
        self._sender_signal = None

    def setEmitter(self, emitter):
        self._sender_signal = emitter

    def getEmitter(self):
        return self._sender_signal


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
        ManagerSignal().setEmitter(self._instance)
        for hand, flags in self._handlers[self._instance]:
            hand(*args, **kwargs)
            if flags & self.FlagConnect.OneShotConnect:
                self.disconnect(hand)
        ManagerSignal().setEmitter(None)