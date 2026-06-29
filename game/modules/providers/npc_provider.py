from game.modules.providers.base_provider import IServiceProvider
from game.modules.npc.system import NpcSystem
from game.modules.npc.behaviors.build import BehaviorBuild
from game.core.system_priority import SystemPriority

class NpcServiceProvider(IServiceProvider):
    def register(self, container):
        pass

    def boot(self, container):
        kernel, event_bus = self.get_core_deps(container)

        npc_system = NpcSystem(kernel, event_bus)
        container.singleton("NpcSystem", npc_system)

        # Register NPC behaviors as Strategies
        kernel.register_strategy("BUILD", BehaviorBuild)

        container.tag("gameplay_update", ["NpcSystem"], priority=SystemPriority.AI_DECISION)
