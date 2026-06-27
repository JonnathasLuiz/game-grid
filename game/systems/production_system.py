from typing import Dict
from ..models.structures import Enterprise, Building, ResourceType

class ProductionSystem:
    def __init__(self, enterprises: Dict[str, Enterprise], buildings: Dict[str, Building]):
        self.enterprises = enterprises
        self.buildings = buildings

    def update(self, delta_ticks: float = 1.0):
        for ent_id, ent in self.enterprises.items():
            building = self.buildings.get(ent.building_id)
            if not building:
                continue

            # 1. Personnel validation
            if ent.employees_present <= 0:
                continue

            # 2. Input validation
            if ent.recipe:
                has_inputs = True
                for inp in ent.recipe.inputs:
                    if building.inventory.get_quantity(inp["type"]) < inp["qty"]:
                        has_inputs = False
                        break

                if not has_inputs:
                    # Lack of raw materials
                    continue

                # 3. Space validation (Output)
                # For simplicity, check if total inventory < max_storage
                total_items = sum(building.inventory.items.values())
                if total_items >= building.max_storage:
                    # Bottleneck
                    continue

                # All pass, advance progress
                ent.production_progress += 10.0 * delta_ticks # 10 ticks to finish a cycle

                if ent.production_progress >= 100.0:
                    # Consume inputs
                    for inp in ent.recipe.inputs:
                        building.inventory.remove(inp["type"], inp["qty"])

                    # Produce outputs
                    for outp in ent.recipe.outputs:
                        building.inventory.add(outp["type"], outp["qty"])

                    ent.production_progress = 0.0
