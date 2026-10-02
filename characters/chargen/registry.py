"""Lookups that bind a model's chargen position to its workflow.

``Step`` and ``Workflow`` live in ``workflow``; the definitions build on them and
this module reads the built definitions, so it is safe to import from models.
"""

from . import get_workflow
from .definitions import DETAIL_ONLY_FREEBIE_POSITIONS
from .workflow import Step, Workflow

__all__ = ["FreebiePosition", "Step", "Workflow", "WorkflowViews", "progress_rows"]


def progress_rows(progress):
    """Rows for the chargen step list, numbered by position.

    ``progress`` is ``Workflow.progress()`` (or any list of ``label``/``status``
    dicts). Consecutive steps with the same ``group`` share one row whose
    status is ``current`` if any of its steps is, ``completed`` if all are.
    """
    rows = []
    for number, step in enumerate(progress, 1):
        group = step.get("group")
        if group and rows and rows[-1]["group"] == group:
            rows[-1]["steps"].append(step)
            continue
        rows.append(
            {
                "number": number,
                "label": step["label"],
                "group": group,
                "conditional": bool(step.get("conditional")),
                "steps": [step],
            }
        )
    for row in rows:
        statuses = {step["status"] for step in row["steps"]}
        if "current" in statuses:
            row["status"] = "current"
        elif statuses == {"completed"}:
            row["status"] = "completed"
        else:
            row["status"] = "pending"
    return rows


class WorkflowViews:
    """Class-compatible mapping, also understood by the route-policy inventory."""

    def __get__(self, instance, owner):
        return get_workflow(owner.model_class.type).view_mapping


class FreebiePosition:
    def __get__(self, instance, owner):
        workflow = get_workflow(owner.type)
        return (
            workflow.freebie_step if workflow else DETAIL_ONLY_FREEBIE_POSITIONS.get(owner.type, -1)
        )
