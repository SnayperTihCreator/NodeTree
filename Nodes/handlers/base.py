import abc
from dataclasses import dataclass, field

from Nodes.utils import ManagerSignal


class BaseHandler(abc.ABC):
    pass


@dataclass
class NameSpace:
    timeDelta: float = field(init=False, default=0)
    allTime: float = field(init=False, default=0)


    @property
    def emitter(self):
        return ManagerSignal().getEmitter()
