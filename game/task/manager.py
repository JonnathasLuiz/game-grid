class TaskManager:
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.event_bus.subscribe("NOVA_TAREFA", self._on_new_task)

    def _on_new_task(self, data):
        # In a real system, this would do matchmaking.
        # Here, it just passes it forward as an order.
        # payload can include target_pos, target_id, etc.
        self.event_bus.publish("ORDEM_CRIADA", **data)
