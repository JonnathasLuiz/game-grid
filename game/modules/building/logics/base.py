"""
Base class for building logics, now integrated with the Strategy Framework.
"""
from game.core.strategy.base import StrategyBase

class LogicBase(StrategyBase):
    """
    Interface for building mechanical logic strategies.
    """
    def __init__(self, building, event_bus, grid_system, kernel, **kwargs):
        super().__init__(building, event_bus, grid_system, kernel, **kwargs)
        # Compatibility alias: StrategyBase uses self.owner, LogicBase traditionally used self.building
        self.building = self.owner

    def execute(self, delta_time):
        """
        Logic to be executed every tick.
        """
        pass

    def receive_progress(self, amount, npc_id):
        """
        Optional: Increments progress for buildings that support it.
        """
        pass
