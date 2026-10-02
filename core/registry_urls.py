"""Model URL helpers without importing view code during Django model loading."""

from core.registries import get_registry


class RegistryURLMixin:
    @classmethod
    def _registry(cls):
        return get_registry(cls._meta.app_label)

    def get_absolute_url(self):
        return self._registry().url(type(self), "detail", self.pk)

    def get_update_url(self):
        return self._registry().url(type(self), "update", self.pk)

    @classmethod
    def get_creation_url(cls):
        return cls._registry().url(cls, "create")
