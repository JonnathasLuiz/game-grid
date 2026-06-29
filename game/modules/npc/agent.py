"""
NPC Agent module representing the physical presence of an NPC in the world.
"""
class NpcAgent:
    """
    A shell entity for NPCs.
    Logic is delegated to an injected behavior strategy via Strategy Framework.
    """
    # Declarative Configuration
    allowStrategies = {"BUILD", "IDLE"} # IDLE could be a basic strategy
    strategyStart = None # NPCs might start without a specific task

    def __init__(self, agent_id, x, y):
        self.id = agent_id
        self.state = "IDLE"
        self.logical_cell = (x, y)
        self.inventory = {}
        self.behavior = None

    def set_behavior(self, strategy_instance):
        """
        Swaps the current behavior strategy.
        """
        self.behavior = strategy_instance

    def update(self, delta_time=0):
        """
        Executes the current behavior strategy.
        """
        if self.behavior:
            self.behavior.execute(delta_time)
