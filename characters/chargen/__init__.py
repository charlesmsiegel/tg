"""Public metadata lookup; safe to import while Django models are loading."""

from .definitions import WORKFLOWS


def get_workflow(character_type):
    return WORKFLOWS.get(character_type)
