import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.models.structures import Agent, Building, Enterprise
from game.models.enums import AgentState, BuildingType
from game.core.grid import GridController
from game.systems.npc_system import NPCSystem

def test_npc_commute():
    gc = GridController(10, 10, cell_size=10)
    home = Building(id="home1", type=BuildingType.RESIDENCE, entrance_cell=(0,0))
    work = Building(id="work1", type=BuildingType.FACTORY, entrance_cell=(5,5))
    ent = Enterprise(building_id="work1")

    buildings = {"home1": home, "work1": work}
    enterprises = {"work1": ent}

    npc = Agent(id="npc1", home_building_id="home1", work_building_id="work1",
                logical_cell=(0,0), current_pos=gc.grid_to_world(0,0), movement_speed=1.0)

    system = NPCSystem(gc, buildings, enterprises)

    # Hour 9: Should start commuting to work
    system.update_agent(npc, 9)
    assert npc.state == AgentState.COMMUTING_TO_WORK
    assert len(npc.path_nodes) > 0

    # Simulate movement until reaches work
    ticks = 0
    while npc.state == AgentState.COMMUTING_TO_WORK and ticks < 20:
        system.update_agent(npc, 9)
        ticks += 1

    assert npc.state == AgentState.WORKING
    assert ent.employees_present == 1
    assert npc.logical_cell == (5, 5)

    # Hour 17: Should start commuting to home
    system.update_agent(npc, 17)
    assert npc.state == AgentState.COMMUTING_TO_HOME
    assert ent.employees_present == 0

    # Simulate movement back home
    ticks = 0
    while npc.state == AgentState.COMMUTING_TO_HOME and ticks < 20:
        system.update_agent(npc, 17)
        ticks += 1

    assert npc.state == AgentState.IDLE
    assert npc.logical_cell == (0, 0)

    print("NPC FSM test passed!")

if __name__ == "__main__":
    test_npc_commute()
