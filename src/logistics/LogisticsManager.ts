import { TransportOrder, ResourceType, BuildingType } from '../types';
import { Building } from '../buildings/Building';
import { Enterprise } from '../buildings/Enterprise';

export class LogisticsManager {
  private pendingOrders: TransportOrder[] = [];
  private activeOrders: Map<string, TransportOrder> = new Map();

  public update(buildings: Map<string, Building>) {
    this.matchMake(buildings);
  }

  private matchMake(buildings: Map<string, Building>) {
    const supply: { buildingId: string; type: ResourceType; qty: number }[] = [];
    const demand: { buildingId: string; type: ResourceType; qty: number }[] = [];

    buildings.forEach((building) => {
      // Check for supply
      for (const [type, qty] of Object.entries(building.inventory)) {
        if (qty > 0) {
          supply.push({ buildingId: building.id, type: type as ResourceType, qty });
        }
      }

      // Check for demand (if it's an Enterprise)
      if (building instanceof Enterprise) {
        for (const input of building.recipe.inputs) {
          const currentStock = building.getStock(input.type);
          if (currentStock < input.qty * 2) { // Demand if less than 2x recipe qty
            demand.push({ buildingId: building.id, type: input.type, qty: input.qty });
          }
        }
      }
    });

    // Simple matchmaking logic
    for (const d of demand) {
      const s = supply.find((s) => s.type === d.type && s.buildingId !== d.buildingId);
      if (s) {
        // Check if an order already exists for this demand to avoid duplicates
        const alreadyOrdered = this.pendingOrders.some(o => o.destinationBuildingId === d.buildingId && o.resourceType === d.type) ||
                               Array.from(this.activeOrders.values()).some(o => o.destinationBuildingId === d.buildingId && o.resourceType === d.type);

        if (!alreadyOrdered) {
          this.createOrder(s.buildingId, d.buildingId, d.type, d.qty);
        }
      }
    }
  }

  private createOrder(originId: string, destId: string, type: ResourceType, qty: number) {
    const order: TransportOrder = {
      id: Math.random().toString(36).substr(2, 9),
      resourceType: type,
      quantity: qty,
      originBuildingId: originId,
      destinationBuildingId: destId,
      status: 'PENDING',
    };
    this.pendingOrders.push(order);
  }

  public getPendingOrder(): TransportOrder | null {
    return this.pendingOrders.shift() || null;
  }

  public assignOrder(orderId: string) {
    // This would move order from pending to assigned if we tracked it that way
  }
}
