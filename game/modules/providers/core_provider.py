from game.modules.providers.base_provider import IServiceProvider
from game.core.event_bus import EventBus
from game.core.grid_system import GridSystem
from game.core.kernel import KernelRegistry
from game.core.system_priority import SystemPriority

class CoreServiceProvider(IServiceProvider):
    def register(self, container):
        event_bus = EventBus()
        grid_system = GridSystem(width=20, height=20)
        kernel = KernelRegistry(event_bus, grid_system)

        container.singleton("EventBus", event_bus)
        container.singleton("GridSystem", grid_system)
        container.singleton("KernelRegistry", kernel)

        # GridSystem doesn't have an update, but if it had, it would be here
        # container.tag("core_update", ["GridSystem"], priority=SystemPriority.PHYSICS_AND_GRID)

    def boot(self, container):
        # Define base execution rules
        container.add_tag_dependency("gameplay_update", depends_on="core_update")
        container.add_tag_dependency("plugin_update", depends_on="gameplay_update")
