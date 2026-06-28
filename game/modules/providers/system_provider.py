from game.modules.providers.base_provider import IServiceProvider
from game.core.system_manager import SystemManager

class SystemServiceProvider(IServiceProvider):
    def register(self, container):
        system_manager = SystemManager(container)
        container.singleton("SystemManager", system_manager)

    def boot(self, container):
        manager = container.resolve("SystemManager")
        manager.build_loop()
