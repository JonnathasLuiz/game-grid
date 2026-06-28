class IServiceProvider:
    """
    Interface for Service Providers.
    """
    def register(self, container):
        """
        Register services and tags.
        """
        pass

    def boot(self, container):
        """
        Configure dependencies and cross-service registrations.
        """
        pass

    def get_core_deps(self, container):
        """
        Utility to resolve common core dependencies.
        """
        return container.resolve("KernelRegistry"), container.resolve("EventBus")
