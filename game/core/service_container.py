from game.core.system_priority import SystemPriority

class ServiceContainer:
    """
    Central dependency injection container and service manager.
    Handles singletons, tagging, and execution order resolution via DAG.
    """
    def __init__(self):
        self._services = {}
        self._tags = {}
        self._tag_dependencies = {} # Maps dependencies. Ex: {"gameplay": ["core"]}

    def singleton(self, service_name: str, instance):
        if service_name in self._services:
            raise KeyError(f"Service '{service_name}' already exists.")
        self._services[service_name] = instance

    def resolve(self, service_name: str):
        if service_name not in self._services:
            raise KeyError(f"Service '{service_name}' not found.")
        return self._services[service_name]

    def tag(self, tags, service_names: list, priority: SystemPriority = SystemPriority.CORE_ENGINE):
        """Assigns one or multiple tags to a list of services with priority."""
        if isinstance(tags, str):
            tags = [tags]

        for tag_name in tags:
            if tag_name not in self._tags:
                self._tags[tag_name] = []
            for name in service_names:
                self._tags[tag_name].append((priority.value, name))

    def add_tag_dependency(self, tag: str, depends_on: str):
        """Defines that 'tag' must run AFTER 'depends_on'."""
        if tag not in self._tag_dependencies:
            self._tag_dependencies[tag] = set()
        self._tag_dependencies[tag].add(depends_on)

    def _topological_sort_tags(self, tags_to_sort: list) -> list:
        """Resolves Macro-Order via Directed Acyclic Graph (DAG)."""
        visited, temp_mark, ordered_tags = set(), set(), []

        def visit(node):
            if node in temp_mark:
                raise RuntimeError(f"Circular dependency detected: '{node}'")
            if node not in visited:
                temp_mark.add(node)

                # Visit required dependencies before adding the node itself
                for dep in self._tag_dependencies.get(node, set()):
                    if dep in tags_to_sort:
                        visit(dep)

                temp_mark.remove(node)
                visited.add(node)
                ordered_tags.append(node)

        for tag in tags_to_sort:
            if tag not in visited:
                visit(tag)

        return ordered_tags

    def resolve_tagged(self, tags) -> list:
        """Resolves multiple tags, applying Macro-Order (DAG) and Micro-Order (Priority)."""
        if isinstance(tags, str):
            tags = [tags]

        # Filter out tags that are not registered
        existing_tags = [t for t in tags if t in self._tags]

        ordered_tags = self._topological_sort_tags(existing_tags)
        final_services, resolved_names = [], set()

        for tag_name in ordered_tags:
            if tag_name not in self._tags: continue

            # Internal sorting (Micro-Order) via SystemPriority
            sorted_entries = sorted(self._tags[tag_name], key=lambda item: item[0])

            for _, service_name in sorted_entries:
                if service_name not in resolved_names:
                    final_services.append(self.resolve(service_name))
                    resolved_names.add(service_name)

        return final_services

    def bootstrap(self, providers: list):
        """Executes the two-phase initialization for a list of Service Providers."""
        for provider in providers:
            provider.register(self)

        for provider in providers:
            provider.boot(self)
