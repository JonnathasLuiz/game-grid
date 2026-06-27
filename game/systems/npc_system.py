from typing import List, Dict, Tuple, Optional
from ..models.structures import Agent, Building, Enterprise
from ..models.enums import AgentState
from ..core.grid import GridController
from ..core.pathfinding import AStarPathfinding
import math

class NPCSystem:
    def __init__(self, grid_controller: GridController, buildings: Dict[str, Building], enterprises: Dict[str, Enterprise]):
        self.gc = grid_controller
        self.buildings = buildings
        self.enterprises = enterprises
        self.pathfinding = AStarPathfinding(grid_controller)

    def update_agent(self, agent: Agent, current_hour: int):
        self._check_state_transitions(agent, current_hour)

        # Always try to reserve current cell to block others
        curr_cell = self.gc.get_cell(agent.logical_cell[0], agent.logical_cell[1])
        if curr_cell and (curr_cell.reservation_id is None or curr_cell.reservation_id == agent.id):
            curr_cell.reservation_id = agent.id

        if agent.state in [AgentState.COMMUTING_TO_WORK, AgentState.COMMUTING_TO_HOME, AgentState.LOGISTICS_TASK]:
            self._move_agent(agent)
        elif agent.state == AgentState.WORKING:
            # Inside building, release any reservation
            if curr_cell and curr_cell.reservation_id == agent.id:
                curr_cell.reservation_id = None

    def _check_state_transitions(self, agent: Agent, current_hour: int):
        if agent.state == AgentState.IDLE or agent.state == AgentState.COMMUTING_TO_HOME:
            if 8 <= current_hour < 17 and agent.work_building_id:
                dest = self.buildings[agent.work_building_id].entrance_cell
                agent.path_nodes = self.pathfinding.find_path_refined(agent.logical_cell, dest)
                if agent.path_nodes:
                    agent.state = AgentState.COMMUTING_TO_WORK
                    if agent.path_nodes[0] == agent.logical_cell:
                        agent.path_nodes.pop(0)

        elif agent.state == AgentState.WORKING:
            if current_hour >= 17 or current_hour < 8:
                enterprise = self.enterprises.get(agent.work_building_id)
                if enterprise: enterprise.employees_present -= 1

                agent.state = AgentState.COMMUTING_TO_HOME
                home = self.buildings.get(agent.home_building_id)
                if home:
                    agent.path_nodes = self.pathfinding.find_path_refined(agent.logical_cell, home.entrance_cell)
                    if agent.path_nodes and agent.path_nodes[0] == agent.logical_cell:
                        agent.path_nodes.pop(0)

    def _move_agent(self, agent: Agent):
        if not agent.path_nodes:
            self._on_reach_destination(agent)
            return

        target_grid = agent.path_nodes[0]
        target_cell = self.gc.get_cell(target_grid[0], target_grid[1])

        # Check if target is reserved by someone else
        if target_cell and target_cell.reservation_id and target_cell.reservation_id != agent.id:
            # If we are already logically in that cell, it's fine (we are just moving to its center)
            if agent.logical_cell != target_grid:
                return # Blocked by other NPC

        # Reserve target
        if target_cell:
            target_cell.reservation_id = agent.id

        target_world = self.gc.grid_to_world(target_grid[0], target_grid[1])
        dx = target_world[0] - agent.current_pos[0]
        dy = target_world[1] - agent.current_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        move_dist = agent.movement_speed * self.gc.cell_size

        old_logical_cell = agent.logical_cell

        if distance <= move_dist:
            agent.current_pos = target_world
            agent.logical_cell = target_grid
            agent.path_nodes.pop(0)
            if not agent.path_nodes:
                self._on_reach_destination(agent)
        else:
            ratio = move_dist / distance
            agent.current_pos = (agent.current_pos[0] + dx * ratio, agent.current_pos[1] + dy * ratio)
            agent.logical_cell = self.gc.world_to_grid(agent.current_pos[0], agent.current_pos[1])

        # If we moved to a new cell, release the old one
        if agent.logical_cell != old_logical_cell:
            old_cell = self.gc.get_cell(old_logical_cell[0], old_logical_cell[1])
            if old_cell and old_cell.reservation_id == agent.id:
                old_cell.reservation_id = None

    def _on_reach_destination(self, agent: Agent):
        # We arrived at the center of the entrance cell.
        if agent.state == AgentState.COMMUTING_TO_WORK:
            agent.state = AgentState.WORKING
            enterprise = self.enterprises.get(agent.work_building_id)
            if enterprise: enterprise.employees_present += 1
            # Release reservation as we "enter"
            cell = self.gc.get_cell(agent.logical_cell[0], agent.logical_cell[1])
            if cell and cell.reservation_id == agent.id: cell.reservation_id = None
        elif agent.state == AgentState.COMMUTING_TO_HOME:
            agent.state = AgentState.IDLE
        elif agent.state == AgentState.LOGISTICS_TASK:
            # Logistics system will handle transition to next phase
            pass
