import { NPCState, Vector2, ResourceType, InventoryObject } from '../types';
import { GridController } from '../core/Grid';

export class Agent {
  public id: string;
  public name: string;
  public current_pos: Vector2; // World coordinates (pixels/float)
  public logical_cell: Vector2; // Grid coordinates
  public home_building_id: string;
  public work_building_id: string | null = null;
  public state: NPCState = NPCState.IDLE;
  public path_nodes: Vector2[] = [];
  public movement_speed: number = 2; // Pixels per tick
  public inventory: { resource_type: ResourceType | null; quantity: number } = {
    resource_type: null,
    quantity: 0,
  };

  private target_cell: Vector2 | null = null;

  constructor(id: string, name: string, startPos: Vector2, home_building_id: string) {
    this.id = id;
    this.name = name;
    this.current_pos = { ...startPos };
    this.logical_cell = { x: Math.floor(startPos.x / 32), y: Math.floor(startPos.y / 32) };
    this.home_building_id = home_building_id;
  }

  public update(grid: GridController) {
    if (this.path_nodes.length > 0) {
      this.moveTowardsTarget(grid);
    }
  }

  private moveTowardsTarget(grid: GridController) {
    const nextNode = this.path_nodes[0];
    const targetWorldPos = grid.gridToWorld(nextNode.x, nextNode.y);

    const dx = targetWorldPos.x - this.current_pos.x;
    const dy = targetWorldPos.y - this.current_pos.y;
    const distance = Math.sqrt(dx * dx + dy * dy);

    if (distance <= this.movement_speed) {
      this.current_pos = targetWorldPos;
      this.logical_cell = nextNode;
      this.path_nodes.shift();

      if (this.path_nodes.length === 0) {
        this.onReachDestination();
      }
    } else {
      this.current_pos.x += (dx / distance) * this.movement_speed;
      this.current_pos.y += (dy / distance) * this.movement_speed;
      this.logical_cell = grid.worldToGrid(this.current_pos.x, this.current_pos.y);
    }
  }

  private onReachDestination() {
    // Logic for when reaching destination
    // This will be handled by the GameLoop or Agent state logic
  }

  public setPath(path: Vector2[]) {
    this.path_nodes = path;
  }

  public clearPath() {
    this.path_nodes = [];
  }
}
