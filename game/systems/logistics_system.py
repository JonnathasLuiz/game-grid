from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Optional, Tuple
from ..models.structures import Agent, Building, ResourceType, Enterprise
from ..models.enums import AgentState
from ..core.grid import GridController
from ..core.pathfinding import AStarPathfinding

class OrderStatus(Enum):
    PENDING = auto()
    PICKING_UP = auto()
    DELIVERING = auto()
    COMPLETED = auto()

@dataclass
class TransportOrder:
    id: str
    resource_type: ResourceType
    quantity: int
    origin_building_id: str
    dest_building_id: str
    status: OrderStatus = OrderStatus.PENDING
    assigned_agent_id: Optional[str] = None

class LogisticsSystem:
    def __init__(self, grid_controller: GridController, buildings: Dict[str, Building], agents: Dict[str, Agent], enterprises: Dict[str, Enterprise] = None):
        self.gc = grid_controller
        self.buildings = buildings
        self.agents = agents
        self.enterprises = enterprises or {}
        self.pathfinding = AStarPathfinding(grid_controller)
        self.orders: List[TransportOrder] = []
        self._order_counter = 0

    def update(self):
        # 1. Matchmaking: connect demand to supply
        self._matchmake()

        # 2. Assign pending orders to idle agents
        self._assign_orders()

        # 3. Process agent logistics tasks
        self._process_tasks()

    def _matchmake(self):
        for dest_id, dest_b in self.buildings.items():
            needed_resources = self._get_building_needs(dest_id)
            if needed_resources:
                # print(f"[Logistics] Building {dest_id} needs {needed_resources}")
                pass
            for res_type, needed_qty in needed_resources.items():
                current_qty = dest_b.inventory.get_quantity(res_type)
                if current_qty < needed_qty:
                    if self._order_already_exists(dest_id, res_type):
                        continue

                    origin_id = self._find_supplier(res_type, needed_qty, dest_id)
                    if origin_id:
                        print(f"[Logistics] Match found! {needed_qty} {res_type.name} from {origin_id} to {dest_id}")
                        self.create_order(res_type, needed_qty, origin_id, dest_id)

    def _get_building_needs(self, building_id: str) -> Dict[ResourceType, int]:
        needs = {}
        enterprise = self.enterprises.get(building_id)
        if enterprise and enterprise.recipe:
            for inp in enterprise.recipe.inputs:
                # Target stock is 2x the recipe requirement
                needs[inp["type"]] = inp["qty"] * 2
        return needs

    def _order_already_exists(self, dest_id: str, res_type: ResourceType) -> bool:
        for o in self.orders:
            if o.dest_building_id == dest_id and o.resource_type == res_type and o.status != OrderStatus.COMPLETED:
                return True
        return False

    def _find_supplier(self, res_type: ResourceType, min_qty: int, skip_id: str) -> Optional[str]:
        for b_id, b in self.buildings.items():
            if b_id == skip_id: continue
            if b.inventory.get_quantity(res_type) >= min_qty:
                return b_id
        return None

    def create_order(self, resource_type: ResourceType, quantity: int, origin_id: str, dest_id: str):
        self._order_counter += 1
        order = TransportOrder(
            id=f"order_{self._order_counter}",
            resource_type=resource_type,
            quantity=quantity,
            origin_building_id=origin_id,
            dest_building_id=dest_id
        )
        self.orders.append(order)

    def _assign_orders(self):
        pending_orders = [o for o in self.orders if o.status == OrderStatus.PENDING]
        if not pending_orders:
            return

        idle_agents = [a for a in self.agents.values() if a.state == AgentState.IDLE]

        for order in pending_orders:
            if not idle_agents:
                break

            origin_b = self.buildings.get(order.origin_building_id)
            if not origin_b: continue

            best_agent = None
            min_dist = float('inf')

            for agent in idle_agents:
                dist = abs(agent.logical_cell[0] - origin_b.entrance_cell[0]) + \
                       abs(agent.logical_cell[1] - origin_b.entrance_cell[1])
                if dist < min_dist:
                    min_dist = dist
                    best_agent = agent

            if best_agent:
                print(f"[Logistics] Assigning {order.id} to {best_agent.name}")
                order.assigned_agent_id = best_agent.id
                order.status = OrderStatus.PICKING_UP
                best_agent.state = AgentState.LOGISTICS_TASK
                best_agent.target_building_id = order.origin_building_id

                best_agent.path_nodes = self.pathfinding.find_path(
                    best_agent.logical_cell, origin_b.entrance_cell
                )
                if best_agent.path_nodes and best_agent.path_nodes[0] == best_agent.logical_cell:
                    best_agent.path_nodes.pop(0)

                idle_agents.remove(best_agent)

    def _process_tasks(self):
        for order in self.orders:
            if order.status == OrderStatus.COMPLETED:
                continue

            if not order.assigned_agent_id:
                continue

            agent = self.agents.get(order.assigned_agent_id)
            if not agent: continue

            target_b_id = agent.target_building_id
            target_b = self.buildings.get(target_b_id)
            if not target_b: continue

            if agent.logical_cell == target_b.entrance_cell and not agent.path_nodes:
                if order.status == OrderStatus.PICKING_UP:
                    origin_b = self.buildings.get(order.origin_building_id)
                    if origin_b.inventory.remove(order.resource_type, order.quantity):
                        agent.inventory.add(order.resource_type, order.quantity)
                        print(f"[Logistics] Agent {agent.name} picked up {order.quantity} {order.resource_type.name}")

                        order.status = OrderStatus.DELIVERING
                        dest_b = self.buildings.get(order.dest_building_id)
                        agent.target_building_id = order.dest_building_id
                        agent.path_nodes = self.pathfinding.find_path(
                            agent.logical_cell, dest_b.entrance_cell
                        )
                        if agent.path_nodes and agent.path_nodes[0] == agent.logical_cell:
                            agent.path_nodes.pop(0)
                    else:
                        # Origin no longer has it?
                        pass

                elif order.status == OrderStatus.DELIVERING:
                    dest_b = self.buildings.get(order.dest_building_id)
                    if agent.inventory.remove(order.resource_type, order.quantity):
                        dest_b.inventory.add(order.resource_type, order.quantity)
                        print(f"[Logistics] Agent {agent.name} delivered {order.quantity} {order.resource_type.name}")

                        order.status = OrderStatus.COMPLETED
                        agent.state = AgentState.IDLE
                        agent.target_building_id = None

        self.orders = [o for o in self.orders if o.status != OrderStatus.COMPLETED]
