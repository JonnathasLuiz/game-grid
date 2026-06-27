import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.core.grid import GridController
from game.models.enums import TerrainType, OccupantType

def test_grid_conversions():
    gc = GridController(10, 10, cell_size=32)

    # Test world_to_grid
    assert gc.world_to_grid(0, 0) == (0, 0)
    assert gc.world_to_grid(31, 31) == (0, 0)
    assert gc.world_to_grid(32, 32) == (1, 1)

    # Test grid_to_world (center of cell)
    assert gc.grid_to_world(0, 0) == (16.0, 16.0)
    assert gc.grid_to_world(1, 1) == (48.0, 48.0)
    print("Grid conversions test passed!")

def test_area_checks():
    gc = GridController(10, 10)
    assert gc.is_area_free(0, 0, 2, 2) == True

    gc.occupy_area(0, 0, 1, 1, OccupantType.BUILDING, "b1")
    assert gc.is_area_free(0, 0, 1, 1) == False
    assert gc.is_area_free(1, 1, 1, 1) == True
    assert gc.is_area_free(0, 0, 2, 2) == False
    print("Area checks test passed!")

if __name__ == "__main__":
    test_grid_conversions()
    test_area_checks()
