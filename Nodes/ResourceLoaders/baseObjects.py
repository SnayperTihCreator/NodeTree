import fnmatch

from Nodes.ResourceLoaders.base import BaseObjectSerialized, BasePropertySerialized

__all__ = ["ObjectResource"]


class ObjectResource(BaseObjectSerialized):
    fileNames = []

    def __setstate__(self, state):
        for k, el in state.items():
            if k == "_className": continue
            if "_classType" in el and el["_classType"] == "Property":
                self.__class__.__dict__[k].__setstate__(el["data"])
                continue
            setattr(self, k, el)

    def __getstate__(self):
        print(self.__class__.__dict__)
        properties_name = {
            k: el
            for k, el in self.__class__.__dict__.items()
            if isinstance(el, BasePropertySerialized)
        }
        return super().__getstate__() | self.__dict__ | properties_name

    @classmethod
    def _hasFileName(cls, file):
        for filePat in cls.fileNames:
            if fnmatch.fnmatch(file, filePat): return True
        return False

