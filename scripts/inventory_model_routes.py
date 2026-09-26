"""Read-only item/location route inventory: python scripts/inventory_model_routes.py."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tg.settings")


def inventory(patterns, prefix="", namespaces=()):
    from django.urls import URLResolver

    for pattern in patterns:
        route = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            scope = namespaces + ((pattern.namespace,) if pattern.namespace else ())
            yield from inventory(pattern.url_patterns, route, scope)
        elif namespaces and namespaces[0] in {"items", "locations"}:
            view = getattr(pattern.callback, "view_class", pattern.callback)
            yield {
                "name": ":".join((*namespaces, pattern.name or "")),
                "path": route,
                "view": f"{view.__module__}.{view.__name__}",
            }


if __name__ == "__main__":
    import django
    from django.urls import get_resolver

    django.setup()
    print(json.dumps(list(inventory(get_resolver().url_patterns)), indent=2))
