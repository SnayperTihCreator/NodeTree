from pygame.sprite import Sprite as _spr, Group as _gr
import pygame as _pg
import pygame.freetype as _ffont
import pygame.geometry as gm
from overloads import OverloadCount
import dataclasses as _ds
from OldNodes import *


class PaintDevice(_spr):
    @_ds.dataclass
    class Stylus:
        font: _ffont.Font | None = None
        color: _ds.InitVar[_pg.Color | int | str | tuple[int]] = 0x000
        size: _ds.InitVar[int] = 20

        def __post_init__(self, color, size):
            self.font = _ffont.Font(None, size, ucs4=True) if self.font is None else self.font
            self.font.fgcolor = _pg.Color(color) if not isinstance(color, _pg.Color) else color

    @_ds.dataclass
    class Brush:
        wight: int = 1
        color: _pg.Color | int | str | tuple[int] = 0x000

        def __post_init__(self):
            if not isinstance(self.color, _pg.Color):
                self.color = _pg.Color(self.color)

    class Painter:
        def __init__(self, src):
            self._src = src
            self.brush = PaintDevice.Brush()
            self.stylus = PaintDevice.Stylus()

        def drawSurface(self, surf, dest):
            self._src.blit(surf, dest)

        def drawLine(self, point1, point2):
            _pg.draw.line(self._src, self.brush.color, point1, point2, self.brush.wight)

        def drawRect(self, rect, bradius=-1):
            _pg.draw.rect(self._src, self.brush.color, rect, self.brush.wight, bradius)

        @OverloadCount
        def drawCircle(self, center, radius):
            _pg.draw.circle(self._src, self.brush.color, center, radius, self.brush.wight)

        @drawCircle.register
        def drawCircle(self, circle: gm.Circle):
            _pg.draw.circle(self._src, self.brush.color, circle.center, circle.radius, self.brush.wight)

        def drawEllipse(self, rect):
            _pg.draw.ellipse(self._src, self.brush.color, rect, self.brush.wight)

        def drawText(self, text, pos):
            self.stylus.font.render_to(self._src, pos, text)

    def __init__(self, node, style: Style, drawing=True):
        super().__init__()
        self.node = node
        self.style = style
        self.layer = self.node.layer
        self.visible = self.node.visible
        self.node.updated.connect(self.handled)
        self.paintDevices = []
        self.drawing = drawing

    def add_device(self, node):
        self.paintDevices.append(PaintDevice(node, self.style, False))
        return self.paintDevices[-1]

    def draw(self, surf: _pg.Surface):
        opt: StyleOption = self.node.delegate.opt(surf, self.style)
        base = self.node.delegate.render(opt.copy())
        [dvs.draw(base)
         for dvs in sorted(self.paintDevices, key=lambda x: x.layer)
         if dvs.visible]
        paint = self.Painter(base)
        self.node.draw(paint)
        return surf.blit(base, opt.rect)

    def handled(self, **kwargs):
        self.visible = kwargs.get("visible", self.visible)
        self.layer = kwargs.get("layer", self.layer)


class DelegateNode:
    def __init__(self, obj):
        self.instance: Node = obj

    def opt(self, surf, style: Style):
        pass

    def render(self, opt: StyleOption):
        pass

    def render_to(self, src: _pg.Surface, opt: StyleOption):
        pass


class Node(_spr):
    updated = Signal()

    def __init__(self, layer, parent=None):
        super().__init__()
        self.delegate = DelegateNode(self)
        self.__layer = layer
        self.__visible = True
        self.__image = None
        self.parent = parent
        if parent is not None:
            self.parent._children.append(self)
        self._children = []

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def children(self):
        return self._children[:]

    @property
    def layer(self):
        return self.__layer

    @layer.setter
    def layer(self, value):
        self.__layer = value
        self.update(layer=value)

    @property
    def visible(self):
        return self.__visible

    @visible.setter
    def visible(self, value):
        self.__visible = value
        self.update(visible=value)

    def draw(self, paint: PaintDevice.Painter):
        raise NotImplementedError

    def update(self, **kwargs):
        self.updated.emit(**kwargs)

    def __init_subclass__(cls, **kwargs):
        cls.name_cls = cls.__name__


class DelegateNode2D(DelegateNode):

    def opt(self, surf, style: Style):
        return StyleOption(self.instance.rect, self.instance.image, surf)

    def render(self, opt: StyleOption):
        surf = _pg.Surface(opt.rect.size, _pg.SRCALPHA)
        surf.fill(0x00000000)
        opt.rect.topleft = (0, 0)
        self.render_to(surf, opt)
        return surf

    def render_to(self, src: _pg.Surface, opt: StyleOption):
        return src.blit(opt.image, opt.rect)


class Node2D(Node):

    def __init__(self, rect, layer=1, parent=None):
        super().__init__(layer, parent)
        self.__rect = rect
        self.delegate = DelegateNode2D(self)

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self, value):
        if isinstance(value, _pg.Rect):
            self.__rect = value

    def draw(self, paint: PaintDevice.Painter):
        pass


@_ds.dataclass
class WindowSetting:
    size: _pg.Vector2
    fps: int = 60
    flags: int = 0
    window: _pg.Surface = None

    def __post_init__(self):
        self.window = _pg.display.set_mode(self.size, self.flags)


class NodeTree(metaclass=MetaSingtoon):
    updateEndFrame = Signal()

    def __init__(self, tManager, windowSetting: WindowSetting):
        self.manager: ManagerNode = tManager
        self.currentScena: BaseScena = None
        self.clock = _pg.time.Clock()
        self.active = True
        self.fps = windowSetting.fps
        self.window = windowSetting.window

    def createGroupNode(self, popup=False):
        return NodeGroup(popup=popup, manager=self.manager)

    def run(self):
        ManagerThread().runGameThread()
        while self.active:
            self.currentScena.drawUpEvent(self.window)
            for e in _pg.event.get():
                if e.type == _pg.QUIT:
                    self.active = False

                self.currentScena.event(e)
            delta = self.clock.get_time() / 1000
            self.currentScena.process(delta)
            self.manager.updateVisible(tick=delta)
            self.currentScena.draw(self.window)
            self.updateEndFrame.emit()
            self.clock.tick(self.fps)
            _pg.display.flip()

    def switch_scena(self, scena):
        _pg.event.post(_pg.Event(NodeTypeEvent.SCENAEXIT, scena=self.currentScena))
        lastScena = self.currentScena
        self.currentScena = scena
        _pg.event.post(_pg.Event(NodeTypeEvent.SCENAENTER, scena=scena))
        return lastScena, scena


class BaseScena:
    def __init__(self):
        self.groups = []

    def createGroup(self):
        grp = self.nodeTree().createGroupNode()
        self.groups.append(grp)
        return grp

    def add_group(self, grp):
        self.groups.append(grp)

    def event(self, e):
        if e.type == NodeTypeEvent.SCENAENTER and e.scena == self:
            self.enter_tree()
        elif e.type == NodeTypeEvent.SCENAEXIT and e.scena == self:
            self.exit_tree()
        [grp.update(event=e) for grp in self.groups]

    def enter_tree(self):
        [grp.switch_focus(True) for grp in self.groups]
        self.nodeTree().manager.updateVisible(beginFrame=None)

    def exit_tree(self):
        [grp.switch_focus(False) for grp in self.groups]
        self.nodeTree().manager.updateVisible(endFrame=None)

    def process(self, delta):
        pass

    def exit_tree(self):
        _pg.event.post(_pg.Event(_pg.QUIT))

    def nodeTree(self):
        return NodeTree(None, None)

    def drawUpEvent(self, surf):
        [grp.draw(surf) for grp in self.groups if grp.popup]

    def draw(self, surf):
        [grp.draw(surf) for grp in self.groups if not grp.popup]


class NodeGroup(_gr):
    def __init__(self, *sprites, visible=True, popup=False, manager: ManagerNode = None):
        self.manager = manager
        self.popup = popup
        self.__visible = visible
        self.__focus = False
        if self.manager is not None:
            self.manager.add_group(self)
        super().__init__(*sprites)

    def add_internal(self, node, layer=None):
        pd = PaintDevice(node, self.manager.style) if node.parent is None else self.spritedict[node.parent].add_device(
            node)
        self.spritedict[node] = pd

    def getDeviceNode(self, node):
        return self.spritedict[node]

    def setDeviceNode(self, node, dvs):
        del self.spritedict[node]
        self.spritedict[node] = dvs

    @property
    def visible(self):
        return self.__visible and self.__focus

    @visible.setter
    def visible(self, value):
        self.__visible = value

    def paintDevices(self) -> list:
        return list(self.spritedict.values())

    def draw(self, surface):
        if self.visible:
            return [dvs.draw(surface)
                    for dvs in sorted(self.paintDevices(), key=lambda x: x.layer)
                    if dvs.visible and dvs.drawing]
        else:
            return None

    def switch_focus(self, status):
        self.__focus = status
