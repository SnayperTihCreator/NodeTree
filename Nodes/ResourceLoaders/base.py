import abc
from enum import IntEnum

import yaml

from Nodes.utils.contexBase import *


class StatusError(IntEnum):
    NoError = 0
    Corrective = 1
    Error = 2


class ContextResource(BaseContext):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.error_msg = ""
        self.newValue = None


class _CMR(BaseContextMachina):
    defaultContext = ContextResource


cmResource = _CMR("ResourceLoader")


def get_context() -> ContextResource:
    return cmResource.get_context()


def set_context(cxt):
    cmResource.set_context(cxt)


class CMResource(BaseContextManager):
    def __init__(self, cxt):
        super().__init__(cmResource, cxt)


class MyYAMLLoader(yaml.Loader):
    def __init__(self, stream):
        super().__init__(stream)
        self.add_multi_constructor("!property", self._property_constructor)
        self.add_multi_constructor("!objectR", self._object_constructor)

    @staticmethod
    def _property_constructor(loader:yaml.Loader, _, node):
        return {"_classType": "Property",
                "data": loader.construct_mapping(node)}

    @staticmethod
    def _object_constructor(loader:yaml.Loader, _, node):
        data = loader.construct_mapping(node)
        cls = BaseObjectSerialized._OBJ_CLASSES[data["_className"]]
        return loader.construct_yaml_object(node, cls)


class MyYAMLDumper(yaml.Dumper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_multi_representer(BasePropertySerialized, self._property_representer)
        self.add_multi_representer(BaseObjectSerialized, self._object_representer)

    @staticmethod
    def _property_representer(dumper: yaml.Dumper, data):
        return dumper.represent_yaml_object("!property", data, BasePropertySerialized)

    @staticmethod
    def _object_representer(dumper:yaml.Dumper, data):
        return dumper.represent_yaml_object("!objectR", data, BaseObjectSerialized)


class BaseObjectSerialized(abc.ABC):
    _OBJ_CLASSES = {}

    @abc.abstractmethod
    def __getstate__(self):
        return {
            "_className": self.__class__.__name__
        }

    @abc.abstractmethod
    def __setstate__(self, state): ...

    def __init_subclass__(cls, **kwargs):
        cls._OBJ_CLASSES[cls.__name__] = cls

class BasePropertySerialized(abc.ABC):
    def __init__(self):
        self._values = {}
        self._instance = None

    @property
    def value(self):
        return self._values[self._instance]

    def __get__(self, instance, owner):
        self._instance = instance
        return self.value

    def __set__(self, instance, value):
        self._instance = instance
        self.value = value

    @abc.abstractmethod
    def __getstate__(self): ...

    @abc.abstractmethod
    def __setstate__(self, state): ...

    @value.setter
    def value(self, value):
        match self._validate(value):
            case StatusError.Error:
                raise TypeError(get_context().error_msg)
            case StatusError.Corrective:
                value = get_context().newValue
        self._values[self._instance] = value
    @classmethod
    @abc.abstractmethod
    def validate(cls, value):
        return StatusError.NoError

    @classmethod
    def _validate(cls, value):
        result = cls.validate(value)
        match result:
            case StatusError.Error:
                get_context().error_msg = cls.eventValidateError(value)
            case StatusError.Corrective:
                get_context().newValue = cls.eventValidateCorrective(value)

        return result

    @classmethod
    def eventValidateError(cls, value):
        return "Error"

    @classmethod
    def eventValidateCorrective(cls, value):
        return value
