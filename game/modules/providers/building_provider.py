from game.modules.providers.base_provider import IServiceProvider
from game.modules.building.system import BuildingSystem
from game.modules.building.logics.blueprint import LogicBlueprint
from game.modules.building.logics.factory import LogicFactory
from game.core.system_priority import SystemPriority

class BuildingServiceProvider(IServiceProvider):
    def register(self, container):
        pass

    def boot(self, container):
        kernel, event_bus = self.get_core_deps(container)

        building_system = BuildingSystem(kernel, event_bus)
        container.singleton("BuildingSystem", building_system)

        # Register Building Logics as Strategies
        kernel.register_strategy("BLUEPRINT", LogicBlueprint)
        kernel.register_strategy("FACTORY", LogicFactory)

        container.tag("gameplay_update", ["BuildingSystem"], priority=SystemPriority.ECONOMY_SYSTEMS)
