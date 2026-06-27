from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from .enums import TerrainType, OccupantType, BuildingType, AgentState, ResourceType
import uuid

@dataclass
class Cell:
    x: int
    y: int
    terrain_type: TerrainType
    movement_cost: int
    is_occupied: bool = False
    occupant_type: OccupantType = OccupantType.NONE
    occupant_id: Optional[str] = None
    reservation_id: Optional[str] = None

@dataclass
class Inventory:
    # Basic inventory: mapping resource type to quantity
    items: Dict[ResourceType, int] = field(default_factory=dict)

    def add(self, resource: ResourceType, quantity: int):
        self.items[resource] = self.items.get(resource, 0) + quantity

    def remove(self, resource: ResourceType, quantity: int) -> bool:
        if self.items.get(resource, 0) >= quantity:
            self.items[resource] -= quantity
            return True
        return False

    def get_quantity(self, resource: ResourceType) -> int:
        return self.items.get(resource, 0)

@dataclass
class Building:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: BuildingType = BuildingType.RESIDENCE
    anchor_x: int = 0
    anchor_y: int = 0
    width: int = 1
    height: int = 1
    entrance_cell: Tuple[int, int] = (0, 0)
    inventory: Inventory = field(default_factory=Inventory)
    max_storage: int = 100

@dataclass
class Recipe:
    inputs: List[Dict[str, any]] # e.g. [{"type": ResourceType.WOOD, "qty": 2}]
    outputs: List[Dict[str, any]] # e.g. [{"type": ResourceType.FURNITURE, "qty": 1}]

@dataclass
class Enterprise:
    building_id: str
    employees: List[str] = field(default_factory=list) # List of NPC IDs
    max_employees: int = 5
    recipe: Optional[Recipe] = None
    production_progress: float = 0.0
    employees_present: int = 0

@dataclass
class Agent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    current_pos: Tuple[float, float] = (0.0, 0.0)
    logical_cell: Tuple[int, int] = (0, 0)
    home_building_id: Optional[str] = None
    work_building_id: Optional[str] = None
    state: AgentState = AgentState.IDLE
    path_nodes: List[Tuple[int, int]] = field(default_factory=list)
    movement_speed: float = 0.1 # grid cells per tick
    inventory: Inventory = field(default_factory=Inventory)
    target_building_id: Optional[str] = None # For logistics/navigation
