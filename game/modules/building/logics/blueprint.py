"""
Blueprint logic for buildings under construction.
"""
from .base import LogicBase

class LogicBlueprint(LogicBase):
    """
    Handles construction progress for a building.
    Transmutes into LogicFactory once 100% progress is reached.
    """
    def __init__(self, building, event_bus, grid_system, kernel, **kwargs):
        super().__init__(building, event_bus, grid_system, kernel, **kwargs)
        self.progress = 0
        self.is_completed = False

    def receive_progress(self, amount, npc_id):
        """
        Increments construction progress and handles completion.
        """
        if self.is_completed:
            return

        self.progress += amount
        print(f"Building {self.building.id} progress: {self.progress}%")

        if self.progress >= 100:
            self.is_completed = True

            # Transmute to FACTORY via the Strategy Framework
            new_logic = self.kernel.create_strategy("FACTORY", self.building)
            self.building.set_logic(new_logic)

            # Notify task completion
            self.event_bus.publish("TAREFA_CONCLUIDA",
                                   target_id=self.building.id,
                                   npc_id=npc_id)
            print(f"Building {self.building.id} construction completed and transmuted to FACTORY!")

    def execute(self, delta_time):
        pass
