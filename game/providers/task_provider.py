from game.providers.base_provider import IServiceProvider
from game.task.manager import TaskManager
from game.core.system_priority import SystemPriority

class TaskServiceProvider(IServiceProvider):
    def register(self, container):
        pass

    def boot(self, container):
        event_bus = container.resolve("EventBus")
        task_manager = TaskManager(event_bus)
        container.singleton("TaskManager", task_manager)

        # TaskManager doesn't have an update method in the current implementation,
        # but if it did, it would be tagged here.
        # container.tag("gameplay_update", ["TaskManager"], priority=SystemPriority.LOGISTICS)
