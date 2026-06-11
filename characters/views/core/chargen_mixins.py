"""Mixins for character creation views."""


class ChargenProgressMixin:
    """Mixin that provides chargen_steps context for the progress bar.

    Subclasses define `chargen_step_labels` as a list of (start_status, label)
    tuples. Example: [(1, "Stats"), (3, "Powers"), (6, "Details"), (7, "Freebies")]

    Note on MRO: This mixin accesses `self.object`, which is set by
    UpdateView.get() before get_context_data is called. For FormView-based
    step views where self.object may not exist, the guard
    `getattr(self, "object", None)` prevents AttributeError.
    """

    chargen_step_labels = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = getattr(self, "object", None)
        if self.chargen_step_labels and obj is not None and hasattr(obj, "creation_status"):
            steps = []
            current = obj.creation_status
            for i, (start, label) in enumerate(self.chargen_step_labels):
                # A group of statuses ends where the next group starts
                if i + 1 < len(self.chargen_step_labels):
                    next_start = self.chargen_step_labels[i + 1][0]
                else:
                    next_start = start + 1
                if current >= next_start:
                    status = "completed"
                elif current >= start:
                    status = "current"
                else:
                    status = "pending"
                steps.append({"label": label, "status": status})
            context["chargen_steps"] = steps
        return context
