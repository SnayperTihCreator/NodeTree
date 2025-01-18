import io
import pathlib
import os
import sys


def getProjectPath():
    return os.getcwd()


class Path(os.PathLike):
    def __init__(self, path):
        self._ppath = pathlib.Path(path)
        self._rpath = pathlib.Path(getProjectPath(), *self._ppath.parts[1:])

    def __fspath__(self):
        return self._rpath.__fspath__()

    @property
    def realPath(self):
        return pathlib.Path(self._rpath)

    def open(self, mode='r', buffering=-1, encoding=None,
             errors=None, newline=None):
        return io.open(self, mode, buffering, encoding, errors, newline)


if __name__ == "__main__":
    pass
