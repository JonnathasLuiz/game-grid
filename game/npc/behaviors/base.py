"""
Base class for NPC behaviors.
"""
class BehaviorGeneric:
    """
    Interface for NPC behavior strategies.
    """
    def __init__(self, npc, task_data, event_bus, grid_system):
        self.npc = npc
        self.task_data = task_data
        self.event_bus = event_bus
        self.grid_system = grid_system

    def execute(self):
        """
        Logic to be executed every tick.
        """
        pass
