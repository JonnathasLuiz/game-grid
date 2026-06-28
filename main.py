"""
Main Entry Point and Bootloader for the grid simulation.
"""
import time
from game.core.event_bus import EventBus
from game.core.grid_system import GridSystem
from game.core.kernel import KernelRegistry
from game.npc.system import NpcSystem
from game.npc.behaviors.build import BehaviorBuild
from game.building.system import BuildingSystem
from game.building.logics.blueprint import LogicBlueprint
from game.building.logics.factory import LogicFactory
from game.task.manager import TaskManager

def main():
    """
    Bootstraps the game systems, registers strategies, and runs the tick loop.
    """
    # 1. Instantiate base dependencies
    event_bus = EventBus()
    grid_system = GridSystem(width=20, height=20)

    # 2. Instantiate KernelRegistry
    kernel = KernelRegistry(event_bus, grid_system)

    # 3. Register behaviors and logics (Boot phase)
    kernel.register_npc_behavior("BUILD", BehaviorBuild)
    kernel.register_building_logic("BLUEPRINT", LogicBlueprint)
    kernel.register_building_logic("FACTORY", LogicFactory)

    # 4. Instantiate Manager Systems
    npc_system = NpcSystem(kernel, event_bus)
    building_system = BuildingSystem(kernel, event_bus)
    task_manager = TaskManager(event_bus)

    # Setup Initial State
    npc_system.add_npc("npc_01", 0, 0)
    building_system.add_building("predio_01", "FACTORY_BUILDING", 5, 5, 5, 4, "BLUEPRINT")

    # Trigger Construction Task
    print("Triggering NOVA_TAREFA for predio_01")
    event_bus.publish("NOVA_TAREFA", task_type="BUILD", target_id="predio_01", target_pos=(5, 4))

    # 5. Game Loop (Temporal Loop)
    tick = 0
    max_ticks = 50
    while tick < max_ticks:
        print(f"--- Tick {tick} ---")
        npc_system.update()
        building_system.update()

        # Check if building construction is completed
        if "predio_01" in building_system.buildings and \
           isinstance(building_system.buildings["predio_01"].logic, LogicFactory):
            print("Simulation goal reached: Building is completed!")
            break

        tick += 1

if __name__ == "__main__":
    main()
