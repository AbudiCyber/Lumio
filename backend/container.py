"""
Lumio Service Container

Stores and manages all shared services.
"""


class ServiceContainer:

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        """
        Register a service.
        """
        self._services[name] = service

    def get(self, name):
        """
        Retrieve a service.
        """
        return self._services.get(name)

    def exists(self, name):
        """
        Check whether service exists.
        """
        return name in self._services

    def remove(self, name):
        """
        Remove service.
        """
        self._services.pop(name, None)

    def health(self):
    return {
        "services": len(self._services),
        "status": "ready"
    }