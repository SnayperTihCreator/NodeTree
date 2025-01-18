from contextvars import ContextVar

__all__ = ["BaseContext", "BaseContextMachina", "BaseContextManager"]


class BaseContext:
    def __init__(self, parent=None):
        self.parent: BaseContext = parent

    def copyContext(self):
        return type(self)(self)


class BaseContextMachina:
    defaultContext = BaseContext()

    def __init__(self, name):
        self._cxt = ContextVar(name)

    def get_context(self) -> type(defaultContext):
        try:
            return self._cxt.get()
        except LookupError:
            self.set_context(self.defaultContext)
            return self._cxt.get()

    def set_context(self, cxt):
        return self._cxt.set(cxt)


class BaseContextManager:
    def __init__(self, mch, cxt):
        self.mch = mch
        self.cxt = cxt or self.mch.get_context()
        self.cxt_last = None

    def __enter__(self):
        self.cxt_last = self.mch.get_context()
        self.mch.set_context(self.cxt)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mch.set_context(self.cxt_last)
        self.cxt_last = None