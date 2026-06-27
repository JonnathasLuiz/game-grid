import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.models.structures import Agent, Building, Inventory, ResourceType
from game.models.enums import AgentState, BuildingType
from game.core.grid import GridController
from game.systems.logistics_system import LogisticsSystem, OrderStatus
from game.systems.npc_system import NPCSystem

def test_logistics_flow():
    gc = GridController(10, 10, cell_size=10)
    b1 = Building(id="origin", type=BuildingType.WAREHOUSE, entrance_cell=(0,0))
    b2 = Building(id="dest", type=BuildingType.FACTORY, entrance_cell=(5,5))

    b1.inventory.add(ResourceType.WOOD, 10)

    npc = Agent(id="carrier", logical_cell=(2,2), current_pos=gc.grid_to_world(2,2), movement_speed=1.0)

    buildings = {"origin": b1, "dest": b2}
    agents = {"carrier": npc}

    logistics = LogisticsSystem(gc, buildings, agents)
    npc_sys = NPCSystem(gc, buildings, {}) # No enterprises needed for this test

    logistics.create_order(ResourceType.WOOD, 5, "origin", "dest")

    # 1. Update logistics to assign order
    logistics.update()

    assert npc.state == AgentState.LOGISTICS_TASK
    assert npc.target_building_id == "origin"

    # 2. Move NPC to origin
    ticks = 0
    while npc.target_building_id == "origin" and ticks < 20:
        npc_sys.update_agent(npc, 12) # Midday
        logistics.update()
        ticks += 1

    assert npc.logical_cell == (0, 0)
    assert npc.inventory.get_quantity(ResourceType.WOOD) == 5
    assert b1.inventory.get_quantity(ResourceType.WOOD) == 5
    assert npc.target_building_id == "dest"

    # 3. Move NPC to destination
    ticks = 0
    while npc.state == AgentState.LOGISTICS_TASK and ticks < 20:
        npc_sys.update_agent(npc, 12)
        logistics.update()
        ticks += 1

    assert npc.logical_cell == (5, 5)
    assert npc.inventory.get_quantity(ResourceType.WOOD) == 0
    assert b2.inventory.get_quantity(ResourceType.WOOD) == 5
    assert npc.state == AgentState.IDLE

    print("Logistics flow test passed!")

if __name__ == "__main__":
    test_logistics_flow()
