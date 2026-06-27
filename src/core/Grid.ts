import { Cell, TerrainType, OccupantType, Vector2 } from '../types';

export class GridController {
  private grid: Cell[][];
  private width: number;
  private height: number;
  private cellSize: number;

  constructor(width: number, height: number, cellSize: number = 32) {
    this.width = width;
    this.height = height;
    this.cellSize = cellSize;
    this.grid = [];

    for (let y = 0; y < height; y++) {
      this.grid[y] = [];
      for (let x = 0; x < width; x++) {
        this.grid[y][x] = {
          x,
          y,
          terrain_type: TerrainType.GRASS,
          movement_cost: 3,
          is_occupied: false,
          occupant_type: OccupantType.NONE,
          occupant_id: null,
          reservation_id: null,
        };
      }
    }
  }

  public getCell(x: number, y: number): Cell | null {
    if (x < 0 || x >= this.width || y < 0 || y >= this.height) {
      return null;
    }
    return this.grid[y][x];
  }

  public worldToGrid(worldX: number, worldY: number): Vector2 {
    return {
      x: Math.floor(worldX / this.cellSize),
      y: Math.floor(worldY / this.cellSize),
    };
  }

  public gridToWorld(gridX: number, gridY: number): Vector2 {
    return {
      x: gridX * this.cellSize + this.cellSize / 2,
      y: gridY * this.cellSize + this.cellSize / 2,
    };
  }

  public isAreaFree(startX: number, startY: number, width: number, height: number): boolean {
    for (let y = startY; y < startY + height; y++) {
      for (let x = startX; x < startX + width; x++) {
        const cell = this.getCell(x, y);
        if (!cell || cell.is_occupied || cell.terrain_type === TerrainType.WATER) {
          return false;
        }
      }
    }
    return true;
  }

  public setTerrain(x: number, y: number, terrain: TerrainType) {
    const cell = this.getCell(x, y);
    if (cell) {
      cell.terrain_type = terrain;
      switch (terrain) {
        case TerrainType.ROAD:
          cell.movement_cost = 1;
          break;
        case TerrainType.GRASS:
          cell.movement_cost = 3;
          break;
        case TerrainType.DIRT:
          cell.movement_cost = 2;
          break;
        case TerrainType.WATER:
          cell.movement_cost = Infinity;
          break;
      }
    }
  }

  public occupyArea(startX: number, startY: number, width: number, height: number, occupantId: string, occupantType: OccupantType) {
    for (let y = startY; y < startY + height; y++) {
      for (let x = startX; x < startX + width; x++) {
        const cell = this.getCell(x, y);
        if (cell) {
          cell.is_occupied = true;
          cell.occupant_id = occupantId;
          cell.occupant_type = occupantType;
          cell.movement_cost = Infinity;
        }
      }
    }
  }

  public getWidth(): number { return this.width; }
  public getHeight(): number { return this.height; }
}
