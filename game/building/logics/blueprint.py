from .base import LogicBase

class LogicBlueprint(LogicBase):
    def __init__(self, building, event_bus, grid_system, kernel):
        super().__init__(building, event_bus, grid_system, kernel)
        self.progress = 0
        self.is_completed = False

    def receive_progress(self, amount, npc_id):
        if self.is_completed:
            return

        self.progress += amount
        print(f"Building {self.building.id} progress: {self.progress}%")

        if self.progress >= 100:
            self.is_completed = True
            # Transmute to LogicFactory
            self.building.logic = self.kernel.create_building_logic("FACTORY", self.building)

            self.event_bus.publish("TAREFA_CONCLUIDA",
                                   target_id=self.building.id,
                                   npc_id=npc_id)
            print(f"Building {self.building.id} construction completed and transmuted to FACTORY!")

    def execute(self):
        pass
