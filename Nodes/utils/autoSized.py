from Nodes.utils.signals import Signal
from Nodes.utils.base import AManager


class ManagerAutoSize(AManager):
    resize = Signal()
