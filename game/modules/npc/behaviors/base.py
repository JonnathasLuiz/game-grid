"""
Base class for NPC behaviors, now integrated with the Strategy Framework.
"""
from game.core.strategy.base import StrategyBase

class BehaviorGeneric(StrategyBase):
    """
    Interface for NPC behavior strategies.
    """
    def __init__(self, npc, event_bus, grid_system, kernel, **kwargs):
        super().__init__(npc, event_bus, grid_system, kernel, **kwargs)
        # Consistency: NPC behaviors used task_data passed via kwargs in the new system
        self.npc = self.owner
        self.task_data = kwargs.get("task_data", {})

    def execute(self, delta_time):
        """
        Logic to be executed every tick.
        """
        pass
