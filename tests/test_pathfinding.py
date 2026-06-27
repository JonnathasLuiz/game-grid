import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.core.grid import GridController
from game.core.pathfinding import AStarPathfinding
from game.models.enums import TerrainType

def test_a_star_basic():
    gc = GridController(5, 5)
    pf = AStarPathfinding(gc)

    path = pf.find_path_refined((0, 0), (4, 4))
    assert len(path) > 0
    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)
    print("Basic A* test passed!")

def test_a_star_weights():
    gc = GridController(5, 5)
    pf = AStarPathfinding(gc)

    # Path (0,0) to (2,0)
    # Direct path: (0,0) -> (1,0) -> (2,0)
    # Make (1,0) very expensive
    gc.set_terrain(1, 0, TerrainType.WATER, 100)

    # Alternative path: (0,0) -> (0,1) -> (1,1) -> (2,1) -> (2,0)
    # Costs: (0,1)=3, (1,1)=3, (2,1)=3, (2,0)=3 Total=12
    # Direct cost: (1,0)=100, (2,0)=3 Total=103

    path = pf.find_path_refined((0, 0), (2, 0))
    assert (1, 0) not in path
    assert (1, 1) in path
    print("Weighted A* test passed!")

if __name__ == "__main__":
    test_a_star_basic()
    test_a_star_weights()
