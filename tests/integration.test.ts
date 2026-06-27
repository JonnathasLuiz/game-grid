import { describe, it, expect } from 'vitest';
import { GameLoop } from '../src/simulation/GameLoop';
import { GridController } from '../src/core/Grid';
import { Agent } from '../src/npcs/Agent';
import { Enterprise } from '../src/buildings/Enterprise';
import { BuildingType, Recipe, NPCState, TerrainType } from '../src/types';

describe('GameLoop Integration', () => {
    it('should simulate a full cycle: agent goes to work, produces, and goes home', () => {
        const grid = new GridController(20, 20);
        const loop = new GameLoop(grid);

        const home = new Enterprise('h1', BuildingType.RESIDENCE, 0, 4, 2, 2, { x: 0, y: 3 }, { inputs: [], outputs: [] });
        const factoryRecipe: Recipe = {
            inputs: [{ type: 'WOOD', qty: 1 }],
            outputs: [{ type: 'FURNITURE', qty: 1 }]
        };
        const factory = new Enterprise('f1', BuildingType.FACTORY, 8, 4, 2, 2, { x: 8, y: 3 }, factoryRecipe);
        factory.addItem('WOOD', 10);

        loop.addBuilding(home);
        loop.addBuilding(factory);

        const agent = new Agent('a1', 'John', grid.gridToWorld(0, 3), 'h1');
        agent.work_building_id = 'f1';
        agent.movement_speed = 100; // Instant move
        factory.employees.push(agent.id);
        loop.addAgent(agent);

        // t=1: Starts commute
        loop.tick();
        // Path is about 8-10 cells.
        for (let i = 0; i < 20; i++) loop.tick();

        expect(agent.state).toBe(NPCState.WORKING);
        expect(factory.current_employees_present).toBe(1);

        // Production needs 100 ticks.
        // If agent is working, factory.update() will be called 100 times.
        for (let i = 0; i < 200; i++) loop.tick();

        expect(factory.getStock('FURNITURE')).toBeGreaterThanOrEqual(1);
    });

    it('should handle logistics: one factory produces, another demands, NPC delivers', () => {
        const grid = new GridController(20, 20);
        const loop = new GameLoop(grid);

        const woodCutterRecipe: Recipe = { inputs: [], outputs: [{ type: 'WOOD', qty: 1 }] };
        const woodCutter = new Enterprise('w1', BuildingType.FACTORY, 0, 0, 2, 2, { x: 0, y: 2 }, woodCutterRecipe);
        woodCutter.employees.push('dummy');
        woodCutter.employeeEnter();

        const furnitureFactoryRecipe: Recipe = { inputs: [{ type: 'WOOD', qty: 1 }], outputs: [{ type: 'FURNITURE', qty: 1 }] };
        const furnitureFactory = new Enterprise('f1', BuildingType.FACTORY, 10, 0, 2, 2, { x: 10, y: 2 }, furnitureFactoryRecipe);

        loop.addBuilding(woodCutter);
        loop.addBuilding(furnitureFactory);

        const deliverer = new Agent('a2', 'Carrier', grid.gridToWorld(5, 5), 'h2');
        deliverer.movement_speed = 100;
        loop.addAgent(deliverer);

        // Produce some wood manually
        for (let i = 0; i < 101; i++) woodCutter.update();
        expect(woodCutter.getStock('WOOD')).toBe(1);

        // Tick loop to trigger logistics
        loop.tick();
        expect(deliverer.state).toBe(NPCState.LOGISTICS_TASK);

        // Tick to arrive at origin, pick up, arrive at destination, deliver
        for (let i = 0; i < 50; i++) loop.tick();

        expect(furnitureFactory.getStock('WOOD')).toBeGreaterThanOrEqual(1);
        expect(woodCutter.getStock('WOOD')).toBe(0);
        expect(deliverer.state).toBe(NPCState.IDLE);
    });
});
