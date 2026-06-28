from enum import IntEnum

class SystemPriority(IntEnum):
    INPUT = 0
    CORE_ENGINE = 100           # Ex: GridSystem, Física
    PHYSICS_AND_GRID = 150      # Specific for grid
    ECONOMY_SYSTEMS = 300       # Ex: BuildingSystem
    LOGISTICS = 400             # Ex: TaskManager
    AI_DECISION = 500           # Ex: NpcSystem
    MODS_AND_PLUGINS = 700      # Ex: Sistemas externos
    POST_PROCESSING = 800       # Ex: Clima
    RENDER = 1000
