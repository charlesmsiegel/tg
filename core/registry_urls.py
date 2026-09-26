"""Model URL helpers without importing view code during Django model loading."""


class RegistryURLMixin:
    @classmethod
    def _registry(cls):
        from core.model_registry import get_registry

        return get_registry(cls._meta.app_label)

    def get_absolute_url(self):
        return self._registry().url(type(self), "detail", self.pk)

    def get_update_url(self):
        return self._registry().url(type(self), "update", self.pk)

    @classmethod
    def get_creation_url(cls):
        return cls._registry().url(cls, "create")
