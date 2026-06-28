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
