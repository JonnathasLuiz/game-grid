from game.providers.base_provider import IServiceProvider
from game.npc.system import NpcSystem
from game.npc.behaviors.build import BehaviorBuild
from game.core.system_priority import SystemPriority

class NpcServiceProvider(IServiceProvider):
    def register(self, container):
        # We need dependencies for registration?
        # Usually register should only instantiate and tag.
        # But NpcSystem needs kernel and event_bus.
        # In a strict DI, we resolve them during register if they were registered before,
        # OR we defer instantiation.
        pass

    def boot(self, container):
        kernel = container.resolve("KernelRegistry")
        event_bus = container.resolve("EventBus")

        npc_system = NpcSystem(kernel, event_bus)
        container.singleton("NpcSystem", npc_system)

        kernel.register_npc_behavior("BUILD", BehaviorBuild)

        container.tag("gameplay_update", ["NpcSystem"], priority=SystemPriority.AI_DECISION)
