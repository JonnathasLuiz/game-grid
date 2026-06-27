from typing import List, Tuple, Optional
from ..models.structures import Cell
from ..models.enums import TerrainType, OccupantType

class GridController:
    def __init__(self, width: int, height: int, cell_size: int = 32):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid: List[List[Cell]] = []
        self._initialize_grid()

    def _initialize_grid(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Default terrain: GRASS with movement cost 3
                row.append(Cell(x=x, y=y, terrain_type=TerrainType.GRASS, movement_cost=3))
            self.grid.append(row)

    def set_road(self, x: int, y: int):
        self.set_terrain(x, y, TerrainType.ROAD, 1)

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def world_to_grid(self, world_x: float, world_y: float) -> Tuple[int, int]:
        grid_x = int(world_x // self.cell_size)
        grid_y = int(world_y // self.cell_size)
        return grid_x, grid_y

    def grid_to_world(self, grid_x: int, grid_y: int) -> Tuple[float, float]:
        # Centered in the cell
        world_x = (grid_x * self.cell_size) + (self.cell_size / 2)
        world_y = (grid_y * self.cell_size) + (self.cell_size / 2)
        return world_x, world_y

    def is_area_free(self, start_x: int, start_y: int, width: int, height: int) -> bool:
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                cell = self.get_cell(x, y)
                if cell is None or cell.is_occupied:
                    return False
        return True

    def set_terrain(self, x: int, y: int, terrain_type: TerrainType, movement_cost: int):
        cell = self.get_cell(x, y)
        if cell:
            cell.terrain_type = terrain_type
            cell.movement_cost = movement_cost

    def occupy_area(self, start_x: int, start_y: int, width: int, height: int, occupant_type: OccupantType, occupant_id: str):
        for y in range(start_y, start_y + height):
            for x in range(start_x, start_x + width):
                cell = self.get_cell(x, y)
                if cell:
                    cell.is_occupied = True
                    cell.occupant_type = occupant_type
                    cell.occupant_id = occupant_id
