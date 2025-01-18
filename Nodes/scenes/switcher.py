from typing import Optional, Iterator

from Nodes.scenes.base import BaseScene, BaseSwitcher


class SwitcherScenes(BaseSwitcher):
    def __init__(self):
        self._scenes = {}
        self._current_scene: Optional[BaseScene] = None
        self._name_current_scene = ""
        self.app = None

    def run(self):
        [scene.__initNameSpace__() for scene in self._scenes.values()]

    def getScene(self) -> Iterator[Optional[BaseScene]]:
        if self._current_scene is None: raise RuntimeError("Not set main scene")
        while self._current_scene.eventHandler.running:
            yield self._current_scene
        yield None

    def add_scene(self, name, scene):
        self._scenes[name] = scene

    def remove_scene(self, name):
        return self._scenes.pop(name)

    def set_first_scene(self, name):
        self._name_current_scene = name
        self._current_scene = self._scenes.get(name)
        return self._current_scene is not None

    def switch(self, name):
        pass
