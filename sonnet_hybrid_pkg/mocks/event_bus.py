# minimaler EventBus Shim für Hybrid-Test
class EventBus:
    def __init__(self, *a, **k): pass
    def publish(self, *a, **k): return None
    def subscribe(self, *a, **k): return lambda *a, **k: None
