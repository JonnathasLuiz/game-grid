class KernelRegistry:
    def __init__(self, event_bus, grid_system):
        self.event_bus = event_bus
        self.grid_system = grid_system
        self._npc_behaviors = {}
        self._building_logics = {}

    def register_npc_behavior(self, name, cls):
        self._npc_behaviors[name] = cls

    def register_building_logic(self, name, cls):
        self._building_logics[name] = cls

    def create_npc_behavior(self, name, npc, task_data):
        if name not in self._npc_behaviors:
            raise ValueError(f"NPC Behavior {name} not registered")
        return self._npc_behaviors[name](npc, task_data, self.event_bus, self.grid_system)

    def create_building_logic(self, name, building):
        if name not in self._building_logics:
            raise ValueError(f"Building Logic {name} not registered")
        return self._building_logics[name](building, self.event_bus, self.grid_system, self)
