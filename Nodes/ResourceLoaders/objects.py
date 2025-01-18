import datetime

import pygame as pg

from Nodes.ResourceLoaders.baseObjects import ObjectResource
from Nodes.ResourceLoaders.property import *
from Nodes.utils import Path


class ImageResource(ObjectResource):
    fileNames = ["*.png", "*.jpg"]

    path = PropertyPath
    _dateChange = PropertyDataTime()
    _imgSurface = PropertyNumpy()

    def __init__(self, path):
        self.path = Path(path)
        _timeChange = self.path.realPath.stat().st_mtime
        self._dateChange = datetime.datetime.fromtimestamp(_timeChange)
        self._img = pg.image.load(self.path)
        self._imgSurface = pg.surfarray.array3d(self._img)
