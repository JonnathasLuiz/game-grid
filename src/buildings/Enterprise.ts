import { Building } from './Building';
import { Recipe, BuildingType, Vector2 } from '../types';

export class Enterprise extends Building {
  public employees: string[] = [];
  public current_employees_present: number = 0;
  public max_employees: number;
  public recipe: Recipe;
  public production_progress: number = 0;
  public production_speed: number = 1; // Progress per tick

  constructor(
    id: string,
    type: BuildingType,
    anchor_x: number,
    anchor_y: number,
    width: number,
    height: number,
    entrance_cell: Vector2,
    recipe: Recipe,
    max_employees: number = 5,
    max_storage: number = 100
  ) {
    super(id, type, anchor_x, anchor_y, width, height, entrance_cell, max_storage);
    this.recipe = recipe;
    this.max_employees = max_employees;
  }

  public update() {
    if (this.canProduce()) {
      this.production_progress += this.production_speed;
      if (this.production_progress >= 100) {
        this.completeProduction();
      }
    }
  }

  private canProduce(): boolean {
    // 1. Personnel validation
    if (this.current_employees_present <= 0) return false;

    // 2. Input validation
    for (const input of this.recipe.inputs) {
      if (this.getStock(input.type) < input.qty) return false;
    }

    // 3. Space validation
    for (const output of this.recipe.outputs) {
      const currentTotal = Object.values(this.inventory).reduce((a, b) => a + b, 0);
      if (currentTotal + output.qty > this.max_storage) return false;
    }

    return true;
  }

  private completeProduction() {
    // Consume inputs
    for (const input of this.recipe.inputs) {
      this.removeItem(input.type, input.qty);
    }

    // Produce outputs
    for (const output of this.recipe.outputs) {
      this.addItem(output.type, output.qty);
    }

    this.production_progress = 0;
  }

  public employeeEnter() {
    this.current_employees_present = Math.min(this.current_employees_present + 1, this.employees.length);
  }

  public employeeExit() {
    this.current_employees_present = Math.max(this.current_employees_present - 1, 0);
  }
}
