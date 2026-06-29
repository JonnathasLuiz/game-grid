"""
NPC System module for managing the lifecycle and tasks of NPCs.
"""
from .agent import NpcAgent

class NpcSystem:
    """
    Manager system for all NPCs. Handles task assignment via Strategy Framework.
    """
    def __init__(self, kernel, event_bus):
        self.kernel = kernel
        self.event_bus = event_bus
        self.npcs = {}
        self.event_bus.subscribe("ORDEM_CRIADA", self._on_order_created)
        self.event_bus.subscribe("TAREFA_CONCLUIDA", self._on_task_completed)

    def add_npc(self, agent_id, x, y):
        """
        Creates and registers a new NPC in the system and grid.
        """
        npc = NpcAgent(agent_id, x, y)
        self.npcs[agent_id] = npc
        self.kernel.grid_system.occupy(x, y, agent_id)
        return npc

    def update(self, delta_time=0):
        """
        Ticks all registered NPCs.
        """
        for npc in self.npcs.values():
            npc.update(delta_time)

    def _on_order_created(self, data):
        """
        Matchmaking logic to assign an order to an idle NPC via Strategy Framework.
        """
        task_type = data.get("task_type")

        # Simple matchmaking: find first IDLE NPC
        for npc in self.npcs.values():
            if npc.state == "IDLE":
                npc.state = "DOING_TASK"
                # Use Strategy Framework to create the behavior
                behavior = self.kernel.create_strategy(task_type, npc, task_data=data)
                npc.set_behavior(behavior)
                break

    def _on_task_completed(self, data):
        """
        Handles task completion events to release NPCs back to IDLE state.
        """
        npc_id = data.get("npc_id")
        if npc_id in self.npcs:
            npc = self.npcs[npc_id]
            npc.state = "IDLE"
            npc.set_behavior(None)
