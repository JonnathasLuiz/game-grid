from enum import Enum, auto

class TerrainType(Enum):
    GRASS = auto()
    DIRT = auto()
    WATER = auto()
    ROAD = auto()

class OccupantType(Enum):
    NONE = auto()
    BUILDING = auto()
    DECORATION = auto()
    NATURAL_RESOURCE = auto()

class BuildingType(Enum):
    RESIDENCE = auto()
    FACTORY = auto()
    WAREHOUSE = auto()

class AgentState(Enum):
    IDLE = auto()
    COMMUTING_TO_WORK = auto()
    WORKING = auto()
    COMMUTING_TO_HOME = auto()
    LOGISTICS_TASK = auto()

class ResourceType(Enum):
    NONE = auto()
    WOOD = auto()
    FURNITURE = auto()
    RAW_MATERIAL = auto() # generic for now
