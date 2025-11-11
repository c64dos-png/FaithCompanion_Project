# minimaler StateStore Shim
class StateStore:
    def __init__(self, *a, **k): self._d = {}
    def set(self, k, v): self._d[k]=v
    def get(self, k, default=None): return self._d.get(k, default)
