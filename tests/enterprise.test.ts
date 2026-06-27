import { describe, it, expect } from 'vitest';
import { Enterprise } from '../src/buildings/Enterprise';
import { BuildingType, Recipe } from '../src/types';

describe('Enterprise Production', () => {
  const woodRecipe: Recipe = {
    inputs: [{ type: 'WOOD', qty: 2 }],
    outputs: [{ type: 'FURNITURE', qty: 1 }]
  };

  it('should not produce without employees', () => {
    const factory = new Enterprise('f1', BuildingType.FACTORY, 0, 0, 2, 2, { x: 0, y: 2 }, woodRecipe);
    factory.addItem('WOOD', 10);

    factory.update();
    expect(factory.production_progress).toBe(0);
  });

  it('should not produce without inputs', () => {
    const factory = new Enterprise('f1', BuildingType.FACTORY, 0, 0, 2, 2, { x: 0, y: 2 }, woodRecipe);
    factory.employees.push('a1');
    factory.employeeEnter();

    factory.update();
    expect(factory.production_progress).toBe(0);
  });

  it('should produce when all conditions are met', () => {
    const factory = new Enterprise('f1', BuildingType.FACTORY, 0, 0, 2, 2, { x: 0, y: 2 }, woodRecipe);
    factory.employees.push('a1');
    factory.employeeEnter();
    factory.addItem('WOOD', 2);
    factory.production_speed = 50;

    factory.update();
    expect(factory.production_progress).toBe(50);
    factory.update();
    expect(factory.production_progress).toBe(0); // Finished and reset
    expect(factory.getStock('WOOD')).toBe(0);
    expect(factory.getStock('FURNITURE')).toBe(1);
  });

  it('should stop producing if output storage is full', () => {
    const factory = new Enterprise('f1', BuildingType.FACTORY, 0, 0, 2, 2, { x: 0, y: 2 }, woodRecipe, 5, 2);
    factory.employees.push('a1');
    factory.employeeEnter();
    factory.addItem('WOOD', 2);
    factory.addItem('FURNITURE', 2); // Full

    factory.update();
    expect(factory.production_progress).toBe(0);
  });
});
