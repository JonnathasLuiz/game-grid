"""
Core interface for the Strategy Framework.
"""
from abc import ABC, abstractmethod

class StrategyBase(ABC):
    """
    Interface for all strategies in the simulation.
    Strategies define the behavior of an entity (NPC or Building).
    """
    def __init__(self, owner, event_bus, grid_system, kernel, **kwargs):
        """
        Initializes the strategy with injected dependencies.
        :param owner: The entity that owns this strategy instance.
        :param event_bus: Central event bus for communication.
        :param grid_system: Spatial management system.
        :param kernel: Strategy kernel for further resolutions.
        """
        self.owner = owner
        self.event_bus = event_bus
        self.grid_system = grid_system
        self.kernel = kernel
        self.logic = None  # Placeholder for the logic to be executed each tick

    @abstractmethod
    def execute(self, delta_time):
        """
        Logic to be executed every tick.
        Must be implemented by subclasses.
        """
        pass

    def set_logic(self, strategy_instance):
        """
        Swaps the current mechanical logic strategy.
        Supports Hot-Swapping.
        """
        self.logic = strategy_instance
