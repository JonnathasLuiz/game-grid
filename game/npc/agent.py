"""
NPC Agent module representing the physical presence of an NPC in the world.
"""
class NpcAgent:
    """
    A shell entity for NPCs. Logic is delegated to an injected behavior strategy.
    """
    def __init__(self, agent_id, x, y):
        self.id = agent_id
        self.state = "IDLE"
        self.logical_cell = (x, y)
        self.inventory = {}
        self.behavior = None

    def update(self):
        """
        Executes the current behavior strategy.
        """
        if self.behavior:
            self.behavior.execute()
