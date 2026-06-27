import { describe, it, expect } from 'vitest';
import { GridController } from '../src/core/Grid';
import { Pathfinding } from '../src/core/Pathfinding';
import { TerrainType } from '../src/types';

describe('Pathfinding', () => {
  it('should find a simple path', () => {
    const grid = new GridController(10, 10);
    const pathfinding = new Pathfinding(grid);

    const path = pathfinding.findPath({ x: 0, y: 0 }, { x: 2, y: 2 });
    expect(path).not.toBeNull();
    expect(path![0]).toEqual({ x: 0, y: 0 });
    expect(path![path!.length - 1]).toEqual({ x: 2, y: 2 });
  });

  it('should avoid obstacles', () => {
    const grid = new GridController(10, 10);
    const pathfinding = new Pathfinding(grid);

    // Create a wall
    grid.setTerrain(1, 0, TerrainType.WATER);
    grid.setTerrain(1, 1, TerrainType.WATER);
    grid.setTerrain(1, 2, TerrainType.WATER);

    const path = pathfinding.findPath({ x: 0, y: 1 }, { x: 2, y: 1 });
    expect(path).not.toBeNull();
    // Path should go around the wall
    path!.forEach(node => {
        expect(grid.getCell(node.x, node.y)!.movement_cost).not.toBe(Infinity);
    });
  });

  it('should prefer lower cost paths (roads)', () => {
    const grid = new GridController(10, 10);
    const pathfinding = new Pathfinding(grid);

    // Grass cost is 3. Let's make a road with cost 1.
    // Start (0,0), End (4,0)
    // Direct path: (1,0), (2,0), (3,0) are Grass(3). (4,0) is Road(1).
    // Road path: (0,1), (1,1), (2,1), (3,1), (4,1), (4,0) are Road(1).

    for (let x = 0; x <= 4; x++) {
        grid.setTerrain(x, 1, TerrainType.ROAD);
    }
    grid.setTerrain(0, 0, TerrainType.ROAD);
    grid.setTerrain(4, 0, TerrainType.ROAD);

    const path = pathfinding.findPath({ x: 0, y: 0 }, { x: 4, y: 0 });
    // Cost of direct path (0,0)->(1,0)G->(2,0)G->(3,0)G->(4,0)R is 3+3+3+1 = 10
    // Cost of road path (0,0)->(0,1)R->(1,1)R->(2,1)R->(3,1)R->(4,1)R->(4,0)R is 1+1+1+1+1+1 = 6
    expect(path).toContainEqual({ x: 2, y: 1 }); // Should take the road
  });
});
