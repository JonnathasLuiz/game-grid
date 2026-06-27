"""
Event Bus module for decoupled communication between game systems.
"""
from collections import defaultdict

class EventBus:
    """
    A central message bus that implements the Publish/Subscribe pattern.
    """
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_type, callback):
        """
        Registers a callback function for a specific event type.
        """
        self._subscribers[event_type].append(callback)

    def publish(self, event_type, **kwargs):
        """
        Triggers all registered callbacks for the given event type with provided data.
        """
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(kwargs)
