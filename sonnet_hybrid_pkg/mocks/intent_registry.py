# minimale Intent Registry Shim
class IntentRegistry:
    def dispatch(self, intent, *a, **k):
        return {"dispatched": intent}
