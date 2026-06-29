from game.modules.providers.base_provider import IServiceProvider
from game.core.event_bus import EventBus
from game.core.grid_system import GridSystem
from game.core.strategy.kernel import StrategyKernel
from game.core.system_priority import SystemPriority

class CoreServiceProvider(IServiceProvider):
    def register(self, container):
        event_bus = EventBus()
        grid_system = GridSystem(width=20, height=20)

        # New Strategy-based Kernel
        kernel = StrategyKernel(event_bus, grid_system)

        container.singleton("EventBus", event_bus)
        container.singleton("GridSystem", grid_system)
        container.singleton("KernelRegistry", kernel) # Keeping the name for compatibility

    def boot(self, container):
        # Define base execution rules
        container.add_tag_dependency("gameplay_update", depends_on="core_update")
        container.add_tag_dependency("plugin_update", depends_on="gameplay_update")
