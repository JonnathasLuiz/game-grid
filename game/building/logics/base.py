"""
Base class for building logics.
"""
class LogicBase:
    """
    Interface for building mechanical logic strategies.
    """
    def __init__(self, building, event_bus, grid_system, kernel):
        self.building = building
        self.event_bus = event_bus
        self.grid_system = grid_system
        self.kernel = kernel

    def execute(self):
        """
        Logic to be executed every tick.
        """
        pass
