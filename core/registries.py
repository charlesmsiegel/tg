"""Locate an app's model registry by name, without importing any view code.

Models call this through ``RegistryURLMixin`` while Django is still loading, so
this module imports nothing from the project; the registry module itself is
imported only when first asked for.
"""

from functools import lru_cache
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured


@lru_cache(maxsize=2)
def get_registry(app):
    if app not in {"items", "locations"}:
        raise ImproperlyConfigured(f"Unsupported registry: {app}")
    return import_module(f"{app}.registry").registry
