"""Public metadata lookup; safe to import while Django models are loading.

``characters.models.core.character`` imports this package (through
``registry``) at model-definition time, so nothing here, in ``definitions``,
``predicates`` or ``workflow`` may import a model or a view at module scope.
Views are named by dotted path and resolved when a step is routed.
``core/tests/test_import_graph.py`` enforces this.
"""

from .definitions import WORKFLOWS


def get_workflow(character_type):
    return WORKFLOWS.get(character_type)
