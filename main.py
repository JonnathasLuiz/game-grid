"""
Main Entry Point and Bootloader for the grid simulation.
"""
from game.core.service_container import ServiceContainer
from game.modules.providers.core_provider import CoreServiceProvider
from game.modules.providers.npc_provider import NpcServiceProvider
from game.modules.providers.building_provider import BuildingServiceProvider
from game.modules.providers.task_provider import TaskServiceProvider
from game.modules.providers.system_provider import SystemServiceProvider
from game.modules.building.logics.factory import LogicFactory

def main():
    """
    Bootstraps the game systems using ServiceContainer and Service Providers,
    registers strategies, and runs the tick loop.
    """
    app_container = ServiceContainer()

    # 1. List of Modules
    providers = [
        CoreServiceProvider(),
        NpcServiceProvider(),
        BuildingServiceProvider(),
        TaskServiceProvider(),
        SystemServiceProvider() # Resolves and builds the final execution list
    ]

    # 2. Bootstrap Providers (Register & Boot Phases)
    app_container.bootstrap(providers)

    # Resolve dependencies for initial state setup
    event_bus = app_container.resolve("EventBus")
    npc_system = app_container.resolve("NpcSystem")
    building_system = app_container.resolve("BuildingSystem")
    system_manager = app_container.resolve("SystemManager")

    # Setup Initial State
    npc_system.add_npc("npc_01", 0, 0)
    building_system.add_building("predio_01", "FACTORY_BUILDING", 5, 5, 5, 4, "BLUEPRINT")

    # Trigger Construction Task
    print("Triggering NOVA_TAREFA for predio_01")
    event_bus.publish("NOVA_TAREFA", task_type="BUILD", target_id="predio_01", target_pos=(5, 4))

    # 4. Game Loop (Temporal Loop)
    tick = 0
    max_ticks = 50
    delta_time = 0.016

    print("Motor Inicializado. Iniciando Simulação.")
    while tick < max_ticks:
        print(f"--- Tick {tick} ---")

        # Executes systems in the perfect hierarchy
        system_manager.update_all(delta_time)

        # Check if building construction is completed
        if "predio_01" in building_system.buildings and \
           isinstance(building_system.buildings["predio_01"].logic, LogicFactory):
            print("Simulation goal reached: Building is completed!")
            break

        tick += 1

if __name__ == "__main__":
    main()
