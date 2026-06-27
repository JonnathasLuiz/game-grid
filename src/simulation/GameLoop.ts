import { GridController } from '../core/Grid';
import { Pathfinding } from '../core/Pathfinding';
import { Agent } from '../npcs/Agent';
import { Building } from '../buildings/Building';
import { Enterprise } from '../buildings/Enterprise';
import { LogisticsManager } from '../logistics/LogisticsManager';
import { NPCState, TransportOrder, OccupantType } from '../types';

export class GameLoop {
  private grid: GridController;
  private pathfinding: Pathfinding;
  private agents: Agent[] = [];
  private buildings: Map<string, Building> = new Map();
  private logistics: LogisticsManager;
  private gameTime: number = 0; // Ticks

  private activeTransportOrders: Map<string, TransportOrder> = new Map();

  constructor(grid: GridController) {
    this.grid = grid;
    this.pathfinding = new Pathfinding(grid);
    this.logistics = new LogisticsManager();
  }

  public addAgent(agent: Agent) {
    this.agents.push(agent);
  }

  public addBuilding(building: Building) {
    this.buildings.set(building.id, building);
    this.grid.occupyArea(
      building.anchor_x,
      building.anchor_y,
      building.width,
      building.height,
      building.id,
      OccupantType.BUILDING
    );

    // Ensure entrance cell is not occupied so NPCs can reach it
    const cell = this.grid.getCell(building.entrance_cell.x, building.entrance_cell.y);
    if (cell) {
        cell.is_occupied = false;
        cell.movement_cost = 1; // Entrance is accessible
    }
  }

  public tick() {
    this.gameTime++;

    // 1. Update Logistics
    this.logistics.update(this.buildings);

    // 2. Simulate NPCs
    this.agents.forEach((agent) => {
      this.updateAgentState(agent);
      agent.update(this.grid);
    });

    // 3. Execute Production
    this.buildings.forEach((building) => {
      if (building instanceof Enterprise) {
        building.update();
      }
    });
  }

  private updateAgentState(agent: Agent) {
    // Basic schedule: 0-100 work, 100-200 home (loop)
    const timeInDay = this.gameTime % 200;

    if (agent.state === NPCState.IDLE) {
      // Check for Logistics Task first
      const order = this.logistics.getPendingOrder();
      if (order) {
        this.assignLogisticsTask(agent, order);
        return;
      }

      if (timeInDay > 0 && timeInDay < 100 && agent.work_building_id) {
        this.startCommute(agent, agent.work_building_id, NPCState.COMMUTING_TO_WORK);
      } else if (timeInDay >= 100) {
        this.startCommute(agent, agent.home_building_id, NPCState.COMMUTING_TO_HOME);
      }
    } else if (agent.state === NPCState.WORKING) {
        if (timeInDay >= 100) {
            const workBuilding = this.buildings.get(agent.work_building_id!);
            if (workBuilding instanceof Enterprise) {
                workBuilding.employeeExit();
            }
            this.startCommute(agent, agent.home_building_id, NPCState.COMMUTING_TO_HOME);
        }
    } else if (agent.state === NPCState.COMMUTING_TO_WORK && agent.path_nodes.length === 0) {
        agent.state = NPCState.WORKING;
        const workBuilding = this.buildings.get(agent.work_building_id!);
        if (workBuilding instanceof Enterprise) {
            workBuilding.employeeEnter();
        }
    } else if (agent.state === NPCState.COMMUTING_TO_HOME && agent.path_nodes.length === 0) {
        agent.state = NPCState.IDLE;
    } else if (agent.state === NPCState.LOGISTICS_TASK) {
        this.updateLogisticsTask(agent);
    }
  }

  private startCommute(agent: Agent, destBuildingId: string, newState: NPCState) {
    const destBuilding = this.buildings.get(destBuildingId);
    if (destBuilding) {
      if (agent.logical_cell.x === destBuilding.entrance_cell.x && agent.logical_cell.y === destBuilding.entrance_cell.y) {
          // Already there
          agent.state = newState === NPCState.COMMUTING_TO_WORK ? NPCState.WORKING : NPCState.IDLE;
          if (agent.state === NPCState.WORKING && destBuilding instanceof Enterprise) {
              destBuilding.employeeEnter();
          }
          return;
      }
      const path = this.pathfinding.findPath(agent.logical_cell, destBuilding.entrance_cell);
      if (path) {
        agent.setPath(path);
        agent.state = newState;
      }
    }
  }

  private assignLogisticsTask(agent: Agent, order: TransportOrder) {
    agent.state = NPCState.LOGISTICS_TASK;
    this.activeTransportOrders.set(agent.id, order);

    const originBuilding = this.buildings.get(order.originBuildingId);
    if (originBuilding) {
        const path = this.pathfinding.findPath(agent.logical_cell, originBuilding.entrance_cell);
        if (path) {
            agent.setPath(path);
            order.status = 'ASSIGNED';
        }
    }
  }

  private updateLogisticsTask(agent: Agent) {
    const order = this.activeTransportOrders.get(agent.id);
    if (!order) return;

    if (agent.path_nodes.length === 0) {
        if (order.status === 'ASSIGNED') {
            // Arrived at origin
            const originBuilding = this.buildings.get(order.originBuildingId);
            if (originBuilding && originBuilding.removeItem(order.resourceType, order.quantity)) {
                agent.inventory.resource_type = order.resourceType;
                agent.inventory.quantity = order.quantity;
                order.status = 'PICKED_UP';

                const destBuilding = this.buildings.get(order.destinationBuildingId);
                if (destBuilding) {
                    const path = this.pathfinding.findPath(agent.logical_cell, destBuilding.entrance_cell);
                    if (path) {
                        agent.setPath(path);
                    }
                }
            } else {
                // Failed to pick up
                agent.state = NPCState.IDLE;
                this.activeTransportOrders.delete(agent.id);
                // Return order to logistics?
            }
        } else if (order.status === 'PICKED_UP') {
            // Arrived at destination
            const destBuilding = this.buildings.get(order.destinationBuildingId);
            if (destBuilding) {
                destBuilding.addItem(agent.inventory.resource_type!, agent.inventory.quantity);
                agent.inventory.resource_type = null;
                agent.inventory.quantity = 0;
                order.status = 'COMPLETED';
                agent.state = NPCState.IDLE;
                this.activeTransportOrders.delete(agent.id);
            }
        }
    }
  }
}
