import abc


class MetaSingleton(abc.ABCMeta):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class AManager(metaclass=MetaSingleton):
    @classmethod
    def inst(cls):
        return cls._instance