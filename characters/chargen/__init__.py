"""Public metadata lookup; safe to import while Django models are loading."""


def get_workflow(character_type):
    from .definitions import WORKFLOWS

    return WORKFLOWS.get(character_type)
