class NpcAgent:
    def __init__(self, agent_id, x, y):
        self.id = agent_id
        self.state = "IDLE"
        self.logical_cell = (x, y)
        self.inventory = {}
        self.behavior = None

    def update(self):
        if self.behavior:
            self.behavior.execute()
