"""
Strategy Kernel for managing registration and instantiation of behaviors.
Now integrated with the Service Container.
"""
class StrategyKernel:
    """
    Central hub for the Strategy Framework.
    Validates capabilities and injects dependencies.
    Resolves strategies and core services via ServiceContainer.
    """
    STRATEGY_PREFIX = "strategy:"

    def __init__(self, container):
        """
        Initializes the StrategyKernel with the service container.
        :param container: The ServiceContainer instance for dependency resolution.
        """
        self.container = container

    @property
    def event_bus(self):
        """Resolves EventBus from container."""
        return self.container.resolve("EventBus")

    @property
    def grid_system(self):
        """Resolves GridSystem from container."""
        return self.container.resolve("GridSystem")

    def register_strategy(self, name, cls):
        """
        Registers a strategy class in the service container.
        """
        service_name = f"{self.STRATEGY_PREFIX}{name}"
        self.container.singleton(service_name, cls)

    def create_strategy(self, name, owner, **kwargs):
        """
        Instantiates a strategy resolved from the container if the owner supports it.
        :param name: Registered name of the strategy.
        :param owner: The entity requesting the strategy.
        :raises ValueError: If strategy is not registered or not allowed by the owner.
        """
        service_name = f"{self.STRATEGY_PREFIX}{name}"

        try:
            strategy_cls = self.container.resolve(service_name)
        except KeyError:
            raise ValueError(f"Strategy {name} is not registered in the Service Container.")

        # Declarative Validation
        if not hasattr(owner, "allowStrategies") or name not in owner.allowStrategies:
            owner_name = type(owner).__name__
            raise ValueError(f"Entity {owner_name} does not support strategy {name}.")

        return strategy_cls(owner, self.event_bus, self.grid_system, self, **kwargs)
