import abc


class BaseComponent(abc.ABC):
    _has_removed = True

    def __init__(self):
        pass

    def onRemoved(self):
        if not self._has_removed: raise ValueError("component not remove")

    def __init_subclass__(cls, **kwargs):
        cls._has_removed = kwargs.get("removed", True)


class BaseHandlerComponent(abc.ABC):
    def __init__(self):
        self._components = {}

    def addComponent(self, nameId, component):
        self._components[nameId] = component

    def removeComponent(self, nameId):
        self._components.pop(nameId)
