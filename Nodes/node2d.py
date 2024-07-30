from Nodes.base_node import Node2D, DelegateNode2D
from Nodes.base_sufr import ColorRect, Image
from Nodes.base_data import StyleOption, Style
from pyganim import PygAnimation, STOPPED
import dataclasses as _ds
from itertools import repeat
import pygame as _pg
from random import choice


class ColorNode(Node2D):
    def __init__(self, color, rect, layer=1, parent=None):
        super().__init__(rect, layer, parent)
        self.image = ColorRect(color, rect.size)


class ImageNode(Node2D):
    def __init__(self, path, pos, layer=1, parent=None):
        rect = path.get_rect() if isinstance(path, Image) else Image(path).get_rect()
        super().__init__(rect, layer, parent)
        self.image = (path if isinstance(path, Image) else Image(path))
        self.rect.topleft = pos


class RandImageNode(ImageNode):
    def __init__(self, paths, pos, layer=1, parent=None):
        super().__init__(choice(paths), pos, layer, parent)


@_ds.dataclass(frozen=True)
class AnimationSetting:
    frames: list
    loop: bool = True

    @classmethod
    def fromListSurface(cls, frames, time=100, loop=True):
        return cls(list(zip(frames, repeat(time))), loop)


@_ds.dataclass
class StyleOptionAnimation(StyleOption):
    animation: PygAnimation

    def copy(self):
        return StyleOptionAnimation(self.rect.copy(), self.image.copy(), self.animation.getCopy())


class DelegateAnimationNode(DelegateNode2D):
    def opt(self, style: Style):
        return StyleOptionAnimation(self.instance.rect, self.instance.image, self.instance.imageAnim)

    def render_to(self, src: _pg.Surface, opt: StyleOptionAnimation):
        return opt.animation.blit(src, opt.rect)


class AnimationNode(Node2D):
    def __init__(self, animSet: AnimationSetting, pos, layer=1, parent=None):
        self.imageAnim = PygAnimation(animSet.frames, animSet.loop)
        super().__init__(_pg.Rect(pos, self.imageAnim.getMaxSize()), layer, parent)
        self.delegate = DelegateAnimationNode(self)

    def set_animation(self, animSet: AnimationSetting):
        self.imageAnim = PygAnimation(animSet.frames, animSet.loop)

    @property
    def image(self):
        return self.imageAnim.getCurrentFrame()

    def update(self, **kwargs):
        super().update(**kwargs)
        if "beginFrame" in kwargs:
            self.imageAnim.play()
        if "endFrame" in kwargs:
            self.imageAnim.pause()
