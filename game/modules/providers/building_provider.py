from game.modules.providers.base_provider import IServiceProvider
from game.modules.building.system import BuildingSystem
from game.modules.building.logics.blueprint import LogicBlueprint
from game.modules.building.logics.factory import LogicFactory
from game.core.system_priority import SystemPriority

class BuildingServiceProvider(IServiceProvider):
    def register(self, container):
        pass

    def boot(self, container):
        kernel = container.resolve("KernelRegistry")
        event_bus = container.resolve("EventBus")

        building_system = BuildingSystem(kernel, event_bus)
        container.singleton("BuildingSystem", building_system)

        kernel.register_building_logic("BLUEPRINT", LogicBlueprint)
        kernel.register_building_logic("FACTORY", LogicFactory)

        container.tag("gameplay_update", ["BuildingSystem"], priority=SystemPriority.ECONOMY_SYSTEMS)
