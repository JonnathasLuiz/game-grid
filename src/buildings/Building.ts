import { BuildingType, Vector2, InventoryObject, ResourceType } from '../types';

export class Building {
  public id: string;
  public type: BuildingType;
  public anchor_x: number;
  public anchor_y: number;
  public width: number;
  public height: number;
  public entrance_cell: Vector2;
  public inventory: InventoryObject = {};
  public max_storage: number;

  constructor(
    id: string,
    type: BuildingType,
    anchor_x: number,
    anchor_y: number,
    width: number,
    height: number,
    entrance_cell: Vector2,
    max_storage: number = 100
  ) {
    this.id = id;
    this.type = type;
    this.anchor_x = anchor_x;
    this.anchor_y = anchor_y;
    this.width = width;
    this.height = height;
    this.entrance_cell = entrance_cell;
    this.max_storage = max_storage;
  }

  public addItem(type: ResourceType, qty: number): boolean {
    const currentTotal = Object.values(this.inventory).reduce((a, b) => a + b, 0);
    if (currentTotal + qty > this.max_storage) {
      return false;
    }
    this.inventory[type] = (this.inventory[type] || 0) + qty;
    return true;
  }

  public removeItem(type: ResourceType, qty: number): boolean {
    if ((this.inventory[type] || 0) < qty) {
      return false;
    }
    this.inventory[type] -= qty;
    if (this.inventory[type] === 0) {
      delete this.inventory[type];
    }
    return true;
  }

  public getStock(type: ResourceType): number {
    return this.inventory[type] || 0;
  }

  public isFull(): boolean {
    const currentTotal = Object.values(this.inventory).reduce((a, b) => a + b, 0);
    return currentTotal >= this.max_storage;
  }
}
