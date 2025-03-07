class ClientRegistry:

    """
    This class is responsible for registering clients.
    """

    def __init__(self):
        self._registry = {}

    def register(self, key, client_class):
        self._registry[key] = client_class

    def create(self, key, **kwargs):
        client_class = self._registry.get(key)
        del kwargs['type']
        if not client_class:
            raise ValueError(f"Client not found for key: {key}")
        return client_class(**kwargs)


client_registry = ClientRegistry()