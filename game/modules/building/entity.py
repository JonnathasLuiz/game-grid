"""
Building Entity module representing a structure in the world.
"""
class BuildingEntity:
    """
    A shell entity for buildings.
    Uses the Strategy Framework for mechanical logic.
    """
    # Declarative Configuration
    allowStrategies = {"BLUEPRINT", "FACTORY"}
    strategyStart = "BLUEPRINT"

    def __init__(self, building_id, b_type, x, y, entrance_x, entrance_y):
        self.id = building_id
        self.type = b_type
        self.anchor_x = x
        self.anchor_y = y
        self.entrance_cell = (entrance_x, entrance_y)
        self.inventory = {}
        self.logic = None

    def set_logic(self, strategy_instance):
        """
        Swaps the current mechanical logic strategy.
        Supports Hot-Swapping.
        """
        self.logic = strategy_instance

    def update(self, delta_time=0):
        """
        Executes the current mechanical logic strategy.
        """
        if self.logic:
            self.logic.execute(delta_time)
