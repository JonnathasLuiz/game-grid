import unittest
from game.core.event_bus import EventBus
from game.core.grid_system import GridSystem
from game.core.kernel import StrategyKernel
from game.core.service_container import ServiceContainer
from game.modules.npc.system import NpcSystem
from game.modules.npc.behaviors.build import BehaviorBuild
from game.modules.building.system import BuildingSystem
from game.modules.building.logics.blueprint import LogicBlueprint
from game.modules.building.logics.factory import LogicFactory
from game.modules.task.manager import TaskManager

class TestSimulation(unittest.TestCase):
    def test_construction_flow(self):
        container = ServiceContainer()
        event_bus = EventBus()
        grid_system = GridSystem(width=10, height=10)

        container.singleton("EventBus", event_bus)
        container.singleton("GridSystem", grid_system)

        kernel = StrategyKernel(container)
        container.singleton("KernelRegistry", kernel)

        kernel.register_strategy("BUILD", BehaviorBuild)
        kernel.register_strategy("BLUEPRINT", LogicBlueprint)
        kernel.register_strategy("FACTORY", LogicFactory)

        npc_system = NpcSystem(kernel, event_bus)
        building_system = BuildingSystem(kernel, event_bus)
        task_manager = TaskManager(event_bus)

        npc = npc_system.add_npc("npc_1", 0, 0)
        building = building_system.add_building("b1", "HOUSE", 2, 2, 2, 1)

        # Verify initial states
        self.assertEqual(npc.state, "IDLE")
        self.assertIsInstance(building.logic, LogicBlueprint)

        # Trigger task
        event_bus.publish("NOVA_TAREFA", task_type="BUILD", target_id="b1", target_pos=(2, 1))

        # Run simulation for a few ticks
        for _ in range(50):
            npc_system.update()
            building_system.update()
            if isinstance(building.logic, LogicFactory):
                break

        # Verify completion
        self.assertIsInstance(building.logic, LogicFactory)
        self.assertEqual(npc.state, "IDLE")
        self.assertIsNone(npc.behavior)
        self.assertEqual(npc.logical_cell, (2, 1))

if __name__ == "__main__":
    unittest.main()
