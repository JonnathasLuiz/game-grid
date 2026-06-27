"""
Kernel Registry module for dependency injection and strategy management.
"""
class KernelRegistry:
    """
    Central registry for behaviors and logics.
    Handles instantiation and dependency injection (EventBus, GridSystem).
    """
    def __init__(self, event_bus, grid_system):
        self.event_bus = event_bus
        self.grid_system = grid_system
        self._npc_behaviors = {}
        self._building_logics = {}

    def register_npc_behavior(self, name, cls):
        """
        Registers an NPC behavior class.
        """
        self._npc_behaviors[name] = cls

    def register_building_logic(self, name, cls):
        """
        Registers a building logic class.
        """
        self._building_logics[name] = cls

    def create_npc_behavior(self, name, npc, task_data):
        """
        Instantiates a registered NPC behavior with injected dependencies.
        """
        if name not in self._npc_behaviors:
            raise ValueError(f"NPC Behavior {name} not registered")
        return self._npc_behaviors[name](npc, task_data, self.event_bus, self.grid_system)

    def create_building_logic(self, name, building):
        """
        Instantiates a registered building logic with injected dependencies.
        """
        if name not in self._building_logics:
            raise ValueError(f"Building Logic {name} not registered")
        return self._building_logics[name](building, self.event_bus, self.grid_system, self)
