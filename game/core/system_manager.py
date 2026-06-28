class SystemManager:
    """
    Orchestrates the execution of systems based on tags.
    """
    def __init__(self, container):
        self.container = container
        self.update_systems = []

    def build_loop(self):
        """
        Builds the final list of systems to be updated in the game loop.
        """
        self.update_systems = self.container.resolve_tagged([
            "core_update",
            "gameplay_update",
            "plugin_update"
        ])

    def update_all(self, delta_time=None):
        """
        Executes the update method on all registered systems.
        """
        for system in self.update_systems:
            # Some systems might not take delta_time, but for now we assume they do or it's optional
            if hasattr(system, 'update'):
                try:
                    system.update(delta_time)
                except TypeError:
                    system.update()
