from Nodes.base_data import MetaSingtoon, ManagerThread, Signal, MetaSkipData
from Nodes.base_node import Node2D
import pygame as _pg
from time import sleep
import pygame.geometry as gm


class Layer(metaclass=MetaSkipData):
    def __init__(self, *layers):
        if len(layers) == 1 and hasattr(layers[0], "__iter__"):
            self._layers = set(layers[0])
        self._layers = set(layers)

    def __or__(self, other):
        if isinstance(other, int):
            return Layer(*self._layers, other)
        elif isinstance(other, Layer):
            return Layer(*self._layers, *other._layers)
        return NotImplemented

    def __and__(self, other):
        if isinstance(other, int):
            return other in self._layers
        elif isinstance(other, Layer):
            return bool(self._layers & other._layers)
        return NotImplemented


class Collider:
    crossed = Signal()

    def __init__(self, owner, shape, layer=1, mask=1):
        self.owner = owner
        self.shape = shape
        self.layer = Layer(layer)
        self.mask = Layer(mask)

    def cross(self, coll):
        return self.layer & coll.mask


class Mask(_pg.Mask):
    def __init__(self, rect: _pg.Rect, fill=False):
        super().__init__(rect.size, fill)
        self.position = rect.topleft

    def collidemask(self, mask):
        if not isinstance(mask, Mask): raise TypeError
        offset = _pg.Vector2(mask.position) - _pg.Vector2(self.position)
        return self.overlap(mask, offset.xy)

    @classmethod
    def fromSurface(cls, surf):
        msk = _pg.mask.from_surface(surf)
        res = Mask(_pg.Rect((0, 0), msk.get_rect()))
        res.draw(msk, (0, 0))
        return res


class PhysicEngine(metaclass=MetaSingtoon):
    class ManageShape:
        def __init__(self):
            self.type_priority = {}
            self.convert_table = {}
            self.collide_table = {}

        def registryShape(self, type_shape, priority, func_collide):
            self.type_priority[type_shape] = (priority, func_collide)

        def registryConvert(self, tp1, tp2, func):
            self.convert_table[(tp1, tp2)] = func

        def registryCollideFunc(self, tp1, tp2, func):
            self.collide_table[(tp1, tp2)] = func

        def getColFunc(self, obj1, obj2):
            tps = type(obj1), type(obj2)
            res = self.collide_table.get(tps, False)
            if res:
                return res
            return self.collide_table.get(tps[::-1], False)

        def getConvert(self, obj1, obj2):
            tps = type(obj1), type(obj2)
            return self.convert_table.get(tps, False)

        def collider(self, obj1, obj2):
            pr1, func_col1 = self.type_priority[type(obj1)]
            pr2, func_col2 = self.type_priority[type(obj2)]
            if pr1 == pr2:
                return func_col1(obj1, obj2)
            if pr1 != pr2 and self.getColFunc(obj1, obj2):
                return self.getColFunc(obj1, obj2)(obj1, obj2)
            if pr1 < pr2 and self.getConvert(obj1, obj2):
                obj1conv = self.getConvert(obj1, obj2)(obj1)
                return self.collider(obj1conv, obj2)
            if self.getConvert(obj2, obj1):
                obj2conv = self.getConvert(obj2, obj1)(obj2)
                return self.collider(obj1, obj2conv)

        def colliderListShape(self, obj, objs):
            return [el for el in objs if self.collider(obj, el)]

        def colliderlist(self, coll, colls):
            return [el for el in colls if self.collider(coll.shape, el.shape)]

    def __init__(self, fps=60):
        self.th = ManagerThread().createThreadGame("PhysicEngine", self.updatePhysicData)
        self.running = True
        self.colliders = []
        self.fps = fps
        self.mgr_shape = self.ManageShape()
        self.mgr_shape.registryShape(_pg.Rect, 1, _pg.Rect.colliderect)
        self.mgr_shape.registryShape(Mask, 255, Mask.collidemask)
        self.mgr_shape.registryShape(gm.Circle, 2, gm.Circle.collidecircle)
        self.mgr_shape.registryCollideFunc(gm.Circle, _pg.Rect, gm.Circle.colliderect)
        self.mgr_shape.registryConvert(_pg.Rect, Mask, lambda rect: Mask(rect, True))

        def circle2mask(circle: gm.Circle):
            surf = _pg.Surface(circle.as_rect().size, _pg.SRCALPHA)
            _pg.draw.circle(surf, "#000", circle.center, circle.radius)
            res = Mask.fromSurface(surf)
            res.position = circle.as_rect().topleft
            return res

        self.mgr_shape.registryConvert(gm.Circle, Mask, circle2mask)

    def updatePhysicData(self):
        while self.running:
            for coll in self.colliders:
                coll_cross = self.mgr_shape.colliderlist(coll, self.colliders)
                coll_cross.remove(coll)
                for el in coll_cross:
                    coll.crossed.emit(el)
            sleep(1 / self.fps)

    def createCollider(self, owner, shape, layer=1, mask=1) -> Collider:
        collider = Collider(owner, shape, layer=layer, mask=mask)
        self.colliders.append(collider)
        return collider


class BaseCollisionNode(Node2D):
    crossed = Signal()

    def __init__(self, rect, collider, layer=1):
        super().__init__(rect, layer)
        self.collider: Collider = collider
        self.collider.crossed.connect(lambda coll: self.crossed.emit(coll))


class Area2D(BaseCollisionNode):
    node_entered = Signal()
    rect_entered = Signal()

    def __init__(self, rect, collider, layer=1):
        super().__init__(rect, collider, layer)
        self.collider.crossed.connect(self.colliding)

    def colliding(self, collide):
        self.node_entered.emit(collide.owner)
        self.rect_entered.emit(collide)
