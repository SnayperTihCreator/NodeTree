import abc

from Nodes.baseComponent import BaseHandlerComponent


class BaseSwitcher(abc.ABC):
    @abc.abstractmethod
    def switch(self, name): ...


class BaseScene(BaseHandlerComponent, abc.ABC):
    class Meta:
        colorBackground = ...
    def __init__(self, switcher):
        super().__init__()
        self.switcher = None
        self.eventHandler = None
        self.loopHandler = None
        self.ns = None

    @abc.abstractmethod
    def __event__(self, event): ...

    @abc.abstractmethod
    def __update__(self): ...

    @abc.abstractmethod
    def __preUpdate__(self, timeDelta, allTime): ...

    @abc.abstractmethod
    def __initNameSpace__(self): ...

class BaseTree(BaseHandlerComponent, abc.ABC):
    pass
