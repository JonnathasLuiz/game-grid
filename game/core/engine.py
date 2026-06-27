from typing import Dict, List
from .grid import GridController
from ..models.structures import Agent, Building, Enterprise
from ..systems.npc_system import NPCSystem
from ..systems.production_system import ProductionSystem
from ..systems.logistics_system import LogisticsSystem

class GameEngine:
    def __init__(self, width: int, height: int):
        self.grid_controller = GridController(width, height)
        self.buildings: Dict[str, Building] = {}
        self.enterprises: Dict[str, Enterprise] = {}
        self.agents: Dict[str, Agent] = {}

        self.npc_system = NPCSystem(self.grid_controller, self.buildings, self.enterprises)
        self.production_system = ProductionSystem(self.enterprises, self.buildings)
        self.logistics_system = LogisticsSystem(self.grid_controller, self.buildings, self.agents, self.enterprises)

        self.global_ticks = 0
        self.hours_per_tick = 0.1 # 10 ticks = 1 hour
        self.current_hour = 6.0 # Start at 6 AM

    def add_building(self, building: Building):
        self.buildings[building.id] = building
        # Occupy grid
        self.grid_controller.occupy_area(
            building.anchor_x, building.anchor_y,
            building.width, building.height,
            building.type, building.id
        )

    def add_enterprise(self, enterprise: Enterprise):
        self.enterprises[enterprise.building_id] = enterprise

    def add_agent(self, agent: Agent):
        self.agents[agent.id] = agent
        # Set initial world position
        agent.current_pos = self.grid_controller.grid_to_world(agent.logical_cell[0], agent.logical_cell[1])

    def tick(self):
        # 1. Update Global Time
        self.global_ticks += 1
        self.current_hour = (6.0 + self.global_ticks * self.hours_per_tick) % 24

        # 2. Update Logistics (Matchmaking & Assignment)
        self.logistics_system.update()

        # 3. Simulate NPCs (Movement & State Transitions)
        for agent in self.agents.values():
            self.npc_system.update_agent(agent, int(self.current_hour))

        # 4. Execute Production
        self.production_system.update()

    def get_status(self):
        return {
            "time": f"{int(self.current_hour):02d}:{(int((self.current_hour%1)*60)):02d}",
            "agents": {a.id: {"state": a.state.name, "pos": a.logical_cell} for a in self.agents.values()},
            "production": {e_id: e.production_progress for e_id, e in self.enterprises.items()}
        }
