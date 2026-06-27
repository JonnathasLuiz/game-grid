import { describe, it, expect } from 'vitest';
import { GridController } from '../src/core/Grid';
import { TerrainType, OccupantType } from '../src/types';

describe('GridController', () => {
  it('should initialize with correct dimensions', () => {
    const grid = new GridController(10, 10);
    expect(grid.getWidth()).toBe(10);
    expect(grid.getHeight()).toBe(10);
  });

  it('should correctly convert world to grid coordinates', () => {
    const grid = new GridController(10, 10, 32);
    const coords = grid.worldToGrid(64, 96);
    expect(coords.x).toBe(2);
    expect(coords.y).toBe(3);
  });

  it('should correctly convert grid to world coordinates (center of cell)', () => {
    const grid = new GridController(10, 10, 32);
    const worldPos = grid.gridToWorld(2, 3);
    expect(worldPos.x).toBe(80); // 2 * 32 + 16
    expect(worldPos.y).toBe(112); // 3 * 32 + 16
  });

  it('should correctly identify free and occupied areas', () => {
    const grid = new GridController(10, 10);
    expect(grid.isAreaFree(2, 2, 2, 2)).toBe(true);

    grid.occupyArea(2, 2, 2, 2, 'b1', OccupantType.BUILDING);
    expect(grid.isAreaFree(2, 2, 2, 2)).toBe(false);
    expect(grid.isAreaFree(1, 1, 1, 1)).toBe(true);
    expect(grid.isAreaFree(1, 1, 2, 2)).toBe(false); // overlaps
  });

  it('should correctly set terrain and update movement cost', () => {
    const grid = new GridController(10, 10);
    const cell = grid.getCell(0, 0)!;

    grid.setTerrain(0, 0, TerrainType.ROAD);
    expect(cell.terrain_type).toBe(TerrainType.ROAD);
    expect(cell.movement_cost).toBe(1);

    grid.setTerrain(0, 0, TerrainType.WATER);
    expect(cell.movement_cost).toBe(Infinity);
  });
});
