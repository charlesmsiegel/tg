"""Ordered chargen tasks. A saved integer identifies a task, not a numbered view.

Metadata never imports views until routing needs them. Reordering a workflow
requires migrating unfinished characters; changing its renderer does not.
"""

from collections.abc import Callable
from dataclasses import dataclass

from django.utils.module_loading import import_string


@dataclass(frozen=True)
class Step:
    key: str
    label: str
    view_path: str
    template: str = "characters/core/chargen/form.html"
    skip_if: Callable | None = None
    # Steps sharing a group sit together in the step list: consecutive steps of
    # one group collapse into a single row ("background": gated by a Background).
    group: str | None = None

    @property
    def view(self):
        return import_string(self.view_path)

    def should_skip(self, character):
        return bool(self.skip_if and self.skip_if(character))


@dataclass(frozen=True)
class Workflow:
    steps: tuple[Step, ...]
    # Interactive workflows swap step fragments with htmx and add live
    # validation (see docs/architecture/character-creation.md).
    # The same views and forms serve both modes; only rendering differs.
    interactive: bool = False

    def __post_init__(self):
        keys = [step.key for step in self.steps]
        if len(keys) != len(set(keys)) or keys.count("freebies") != 1:
            raise ValueError("A workflow needs unique keys and exactly one freebies step")

    def step(self, position):
        if not 1 <= position <= len(self.steps):
            raise ValueError(f"Invalid chargen position: {position}")
        return self.steps[position - 1]

    @property
    def freebie_step(self):
        return next(i for i, step in enumerate(self.steps, 1) if step.key == "freebies")

    @property
    def view_mapping(self):
        return {i: step.view for i, step in enumerate(self.steps, 1)}

    def progress(self, position):
        return [
            {
                "key": step.key,
                "label": step.label,
                "status": (
                    "completed" if i < position else "current" if i == position else "pending"
                ),
                # Whether the step can be skipped. Skipping is decided when the
                # step is reached, so the list marks it rather than hiding it.
                "conditional": step.skip_if is not None,
                "group": step.group,
            }
            for i, step in enumerate(self.steps, 1)
        ]
