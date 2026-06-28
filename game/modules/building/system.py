"""
Building System module for managing structures and their progress.
"""
from .entity import BuildingEntity

class BuildingSystem:
    """
    Manager system for all buildings. Listens for progress events.
    """
    def __init__(self, kernel, event_bus):
        self.kernel = kernel
        self.event_bus = event_bus
        self.buildings = {}
        self.event_bus.subscribe("PROGRESSO_GERADO", self._on_progress_generated)

    def add_building(self, building_id, b_type, x, y, entrance_x, entrance_y, logic_name):
        """
        Creates and registers a new building in the system and grid.
        """
        building = BuildingEntity(building_id, b_type, x, y, entrance_x, entrance_y)
        building.logic = self.kernel.create_building_logic(logic_name, building)
        self.buildings[building_id] = building
        self.kernel.grid_system.occupy(x, y, building_id)
        return building

    def update(self):
        """
        Ticks all registered buildings.
        """
        for building in self.buildings.values():
            building.update()

    def _on_progress_generated(self, data):
        """
        Handles progress events and routes them to the appropriate building logic.
        """
        target_id = data.get("target_id")
        amount = data.get("amount")
        npc_id = data.get("npc_id")

        if target_id in self.buildings:
            building = self.buildings[target_id]
            # Building logic is expected to implement receive_progress if it can be constructed/worked on
            if hasattr(building.logic, "receive_progress"):
                building.logic.receive_progress(amount, npc_id)
