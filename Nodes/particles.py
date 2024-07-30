from dataclasses import dataclass, field
from random import randint

import pygame as _pg

from Nodes import ImageNode
from Nodes.base_data import StyleOption, Style
from Nodes.base_node import DelegateNode2D


@dataclass
class ParticleSetting:
    speed: float = 5
    count_shape: int = 10
    min_angle: float = 0
    max_angle: float = 0


@dataclass
class StyleOptionParticle(StyleOption):
    setting: ParticleSetting
    def copy(self):
        return StyleOptionParticle(self.rect.copy(), self.image.copy(), self.screen, self.setting)


class DelegateParticle(DelegateNode2D):
    def __init__(self, node):
        super().__init__(node)
        self._shapes = [node.image.copy() for _ in range(node.setting.count_shape)]
        self._positions = [_pg.Vector2(node.rect.center) for _ in range(node.setting.count_shape)]
        self._directions = [_pg.Vector2(0, 1).rotate(randint(node.setting.min_angle, node.setting.max_angle))
                            for _ in range(node.setting.count_shape)]

    def opt(self, surf, style: Style):
        return StyleOptionParticle(self.instance.rect, self.instance.image, surf, self.instance.setting)

    def render_to(self, src, opt):
        for i, (sps, pos, dirs) in enumerate(zip(self._shapes, self._positions, self._directions)):
            if not opt.rect.collidepoint(pos):
                self._positions[i] = _pg.Vector2(opt.rect.center)
            self._positions[i] += dirs
            src.blit(sps, pos)


class Particle(ImageNode):
    def __init__(self, shape, rect, setting, layer=1, parent=None):
        super().__init__(shape, rect.topleft, layer, parent)
        self.setting = setting
        self.rect = rect
        self.delegate = DelegateParticle(self)
