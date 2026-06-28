"""
Task Manager module for handling logic/economic matchmaking.
"""
class TaskManager:
    """
    Service responsible for converting demand into actionable orders for agents.
    """
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe("NOVA_TAREFA", self._on_new_task)

    def _on_new_task(self, data):
        """
        Processes a task request and publishes a corresponding order.
        """
        # In a real system, this would perform matchmaking between demand and supply.
        self.event_bus.publish("ORDEM_CRIADA", **data)
