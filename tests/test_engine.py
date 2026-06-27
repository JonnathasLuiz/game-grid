import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.core.engine import GameEngine
from game.models.structures import Building, Enterprise, Agent, Recipe, ResourceType
from game.models.enums import BuildingType

def test_engine_integration():
    engine = GameEngine(20, 20)

    # Setup a small world
    home = Building(id="h1", type=BuildingType.RESIDENCE, anchor_x=1, anchor_y=1, entrance_cell=(1,1))
    factory = Building(id="f1", type=BuildingType.FACTORY, anchor_x=5, anchor_y=5, entrance_cell=(5,5))

    recipe = Recipe(inputs=[], outputs=[{"type": ResourceType.WOOD, "qty": 1}])
    ent = Enterprise(building_id="f1", recipe=recipe)

    npc = Agent(id="n1", home_building_id="h1", work_building_id="f1", logical_cell=(1,1), movement_speed=1.0)

    engine.add_building(home)
    engine.add_building(factory)
    engine.add_enterprise(ent)
    engine.add_agent(npc)

    # Run for some ticks
    for _ in range(50):
        engine.tick()
        status = engine.get_status()
        # print(status["time"], status["agents"]["n1"]["state"], status["production"]["f1"])

    # By 50 ticks (5 hours later), it's 11 AM. NPC should be working.
    assert engine.current_hour >= 11.0
    assert npc.state.name == "WORKING"
    assert ent.production_progress > 0

    print("Engine integration test passed!")

if __name__ == "__main__":
    test_engine_integration()
