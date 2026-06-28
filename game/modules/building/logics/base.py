"""
Base class for building logics.
"""
from abc import ABC, abstractmethod

class LogicBase(ABC):
    """
    Interface for building mechanical logic strategies.
    All building logics must inherit from this class.
    """
    def __init__(self, building, event_bus, grid_system, kernel):
        """
        Initializes the logic with injected dependencies.
        """
        self.building = building
        self.event_bus = event_bus
        self.grid_system = grid_system
        self.kernel = kernel

    @abstractmethod
    def execute(self):
        """
        Logic to be executed every tick.
        Must be implemented by subclasses.
        """
        pass

    def receive_progress(self, amount, npc_id):
        """
        Optional: Increments progress for buildings that support it.
        Default implementation does nothing.
        """
        pass
