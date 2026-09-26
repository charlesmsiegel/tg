# URL Patterns

## Directory Structure

```
app/urls/
├── __init__.py           # Main router
└── gameline/
    ├── __init__.py       # Gameline router
    ├── list.py
    ├── detail.py
    ├── create.py
    └── update.py
```

## Main Router

```python
# app/urls/__init__.py (see items/urls/__init__.py)
from importlib import import_module

from django.urls import include, path

from core.constants import GameLine

from .core import create, detail, index, update

urlpatterns = []
for url_path, module_name, namespace in GameLine.URL_PATTERNS:
    try:
        gameline_module = import_module(f".{module_name}", package="app.urls")
        urlpatterns.append(
            path(f"{url_path}/", include((gameline_module.urls, module_name), namespace=namespace))
        )
    except (ImportError, AttributeError):
        pass

urlpatterns.extend(
    [
        path("create/", include((create.urls, "app_create"), namespace="create")),
        path("update/", include((update.urls, "app_update"), namespace="update")),
        path("list/", include((index.urls, "app_list"), namespace="list")),
        path("", include(detail.urls)),
    ]
)
```

## Gameline Router

```python
# app/urls/mygameline/__init__.py (see items/urls/demon/__init__.py)
from django.urls import include, path

from . import create, detail, index, update

urls = [
    path("create/", include((create.urls, "mygameline_create"), namespace="create")),
    path("update/", include((update.urls, "mygameline_update"), namespace="update")),
    path("list/", include((index.urls, "mygameline_list"), namespace="list")),
    path("", include(detail.urls)),
]
```

## Leaf modules (create / update / list / detail)

Each leaf module exports a plain `urls` list. Do **not** add `app_name`: the list is
included directly or as a `(urls, app_name)` tuple, so Django never reads a module-level
`app_name` (`core/tests/test_dead_code_removed.py` fails if one is added).

```python
# app/urls/mygameline/create.py
from django.urls import path

from app import views

urls = [
    path("my_character/", views.mygameline.MyCharacterCreateView.as_view(), name="my_character"),
    path("my_reference/", views.mygameline.MyReferenceCreateView.as_view(), name="my_reference"),
]
```

`update.py` uses `<int:pk>/` paths, `index.py` holds list views, and `detail.py` holds
`<int:pk>/` detail routes, all in the same shape.

## Namespace Convention

```
app:gameline:action:model_type
```

Examples:
- `characters:vampire:detail:vampire`
- `items:mage:create:wonder`
- `locations:werewolf:update:caern`
