from .base import BehaviorGeneric

class BehaviorBuild(BehaviorGeneric):
    def __init__(self, npc, task_data, event_bus, grid_system):
        super().__init__(npc, task_data, event_bus, grid_system)
        self.target_id = task_data["target_id"]
        self.target_pos = task_data["target_pos"] # Entrance cell
        self.state = "CALCULATING_PATH"
        self.path = []

    def execute(self):
        if self.state == "CALCULATING_PATH":
            self.path = self.grid_system.find_path(self.npc.logical_cell, self.target_pos)
            if self.path:
                # Remove start node from path if it's the current cell
                if self.path and self.path[0] == self.npc.logical_cell:
                    self.path.pop(0)
                self.state = "MOVING"
            else:
                # Handle no path found
                pass

        elif self.state == "MOVING":
            if self.path:
                next_pos = self.path.pop(0)
                self.grid_system.release(*self.npc.logical_cell)
                self.npc.logical_cell = next_pos
                self.grid_system.occupy(*next_pos, self.npc.id)

                if self.npc.logical_cell == self.target_pos:
                    self.state = "WORKING"
            else:
                if self.npc.logical_cell == self.target_pos:
                    self.state = "WORKING"

        elif self.state == "WORKING":
            # Emit progress
            self.event_bus.publish("PROGRESSO_GERADO",
                                   target_id=self.target_id,
                                   amount=10,
                                   npc_id=self.npc.id)
