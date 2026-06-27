from collections import defaultdict

class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type, callback):
        self._subscribers[event_type].append(callback)

    def publish(self, event_type, **kwargs):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(kwargs)
