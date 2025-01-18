import numbers
import datetime

import numpy

from Nodes.ResourceLoaders.base import BasePropertySerialized, StatusError
from Nodes.utils import Path


class _PropertyBaseValues(BasePropertySerialized):
    typeCorrective = type
    typeCorrectiveTrue = StatusError.NoError
    typeCorrectiveFalse = StatusError.Error

    def __getstate__(self):
        return {
            "values": self._values
        }

    def __setstate__(self, state):
        self._values = state["values"]
        return self

    @classmethod
    def validate(cls, value):
        return cls.typeCorrectiveTrue if isinstance(value, cls.typeCorrective) else cls.typeCorrectiveFalse

    @classmethod
    def eventValidateError(cls, value):
        return f"Expected {cls.typeCorrective}, but received {type(value)}"


class PropertyNumber(_PropertyBaseValues):
    typeCorrective = numbers.Number


class PropertyString(_PropertyBaseValues):
    typeCorrective = str
    typeCorrectiveFalse = StatusError.Corrective

    @classmethod
    def eventValidateCorrective(cls, value):
        return str(value)


class PropertyFloat(_PropertyBaseValues):
    typeCorrective = float


class PropertyDataTime(_PropertyBaseValues):
    typeCorrective = datetime.datetime


class PropertyNumpy(_PropertyBaseValues):
    typeCorrective = numpy.ndarray


class PropertyPath(_PropertyBaseValues):
    typeCorrective = Path


__all__ = ["PropertyPath", "PropertyNumpy", "PropertyDataTime",
           "PropertyString", "PropertyNumber", "PropertyFloat"]
