"""
Strategy Kernel for managing registration and instantiation of behaviors.
"""
class StrategyKernel:
    """
    Central hub for the Strategy Framework.
    Validates capabilities and injects dependencies.
    """
    def __init__(self, event_bus, grid_system):
        self.event_bus = event_bus
        self.grid_system = grid_system
        self._strategies = {}

    def register_strategy(self, name, cls):
        """
        Registers a strategy class under a unique name.
        """
        self._strategies[name] = cls

    def create_strategy(self, name, owner, **kwargs):
        """
        Instantiates a strategy if the owner supports it.
        :param name: Registered name of the strategy.
        :param owner: The entity requesting the strategy.
        :raises ValueError: If strategy is not registered or not allowed by the owner.
        """
        if name not in self._strategies:
            raise ValueError(f"Strategy {name} is not registered in the Kernel.")

        # Declarative Validation
        if not hasattr(owner, "allowStrategies") or name not in owner.allowStrategies:
            owner_name = type(owner).__name__
            raise ValueError(f"Entity {owner_name} does not support strategy {name}.")

        strategy_cls = self._strategies[name]
        return strategy_cls(owner, self.event_bus, self.grid_system, self, **kwargs)
