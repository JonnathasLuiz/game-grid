from .entity import BuildingEntity

class BuildingSystem:
    def __init__(self, kernel, event_bus):
        self.kernel = kernel
        self.event_bus = event_bus
        self.buildings = {}
        self.event_bus.subscribe("PROGRESSO_GERADO", self._on_progress_generated)

    def add_building(self, building_id, b_type, x, y, entrance_x, entrance_y, logic_name):
        building = BuildingEntity(building_id, b_type, x, y, entrance_x, entrance_y)
        building.logic = self.kernel.create_building_logic(logic_name, building)
        self.buildings[building_id] = building
        # For simplicity, we only occupy the anchor cell in this mock
        self.kernel.grid_system.occupy(x, y, building_id)
        return building

    def update(self):
        for building in self.buildings.values():
            building.update()

    def _on_progress_generated(self, data):
        target_id = data.get("target_id")
        amount = data.get("amount")
        npc_id = data.get("npc_id")

        if target_id in self.buildings:
            building = self.buildings[target_id]
            if hasattr(building.logic, "receive_progress"):
                building.logic.receive_progress(amount, npc_id)
