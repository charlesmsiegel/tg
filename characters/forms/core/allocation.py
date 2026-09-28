"""Forms that enforce ``characters.rules`` point-allocation rules in ``clean()``."""

from functools import cache

from django import forms

from characters.rules.allocation import RANK_SHORT, RANKS, first_violation


class AllocationFormMixin:
    """Validate ``allocation_rules`` (passed as a kwarg) against cleaned data.

    Only the first violation is reported, with the chargen steps' historical
    text. A violation's optional flash text is kept in ``flash_errors`` so the
    step view can repeat it as a ``messages.error`` notice.

    ``extra_clean`` is an optional callable ``(cleaned_data) -> RuleViolation |
    None`` for a check that needs the character, run after every rule passes.

    A priority rule (Attributes, Abilities) also reads one posted choice per
    group (``priority_physical`` ...): the rank the player gave it, from the
    PRI / SEC / TER picker. The choices are not form fields (nothing is saved
    and the model never sees them); a missing or unknown value is no choice,
    and without a complete choice the rule infers the ranking from the dots.
    """

    def __init__(self, *args, allocation_rules=(), extra_clean=None, **kwargs):
        self.allocation_rules = tuple(allocation_rules)
        self.extra_clean = extra_clean
        self.flash_errors = []
        super().__init__(*args, **kwargs)

    def rank_values(self):
        """The posted rank choices, by rank field name (empty when unbound)."""
        if not self.is_bound:
            return {}
        return {
            name: self.data.get(self.add_prefix(name), "")
            for rule in self.allocation_rules
            for name in getattr(rule, "priority_fields", ())
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        values = {**cleaned_data, **self.rank_values()}
        violation = first_violation(self.allocation_rules, values)
        if violation is None and self.extra_clean is not None:
            violation = self.extra_clean(cleaned_data)
        if violation is not None:
            self.add_violation(violation)
        return cleaned_data

    def add_violation(self, violation):
        self.add_error(violation.field, violation.message)
        if violation.flash:
            self.flash_errors.append(violation.flash)


class AllocationModelForm(AllocationFormMixin, forms.ModelForm):
    pass


@cache
def allocation_modelform(model, fields):
    """A ModelForm over ``fields`` (a tuple) whose clean() applies allocation rules."""
    return forms.modelform_factory(model, form=AllocationModelForm, fields=list(fields))


def rating_values(form):
    """Current ratings of a bound form for running totals, even when invalid.

    Cleaned values win; a field that failed cleaning falls back to its raw
    submitted integer (or 0) so totals still reflect what the player typed.
    Posted rank choices (``AllocationFormMixin.rank_values``) are included.
    """
    cleaned = getattr(form, "cleaned_data", {})
    values = {}
    for name in form.fields:
        if name in cleaned:
            values[name] = cleaned[name]
            continue
        try:
            values[name] = int(form.data.get(form.add_prefix(name), ""))
        except (TypeError, ValueError):
            values[name] = 0
    if hasattr(form, "rank_values"):
        values.update(form.rank_values())
    return values


def priority_columns(form, rule):
    """Template context for a priority rule's columns (the PRI / SEC / TER picker).

    Returns ``{"columns": [...], "rule": name, <group>: column}``. Each column
    is ``PriorityRule.columns()`` for the form's current values (bound data, or
    the initial ratings) plus ``field`` (the posted rank's name) and ``options``:
    one per rank with ``value``, ``short``, ``points``, ``target``, ``checked``
    and ``id``, and ``fields``, the group's bound fields. The checked option is
    the posted choice, or the rank the counts use when none was posted.
    """
    if form.is_bound:
        values = rating_values(form)
    else:
        values = {name: form[name].initial for name in form.fields}
    posted = rule.posted_ranks(values)
    columns = rule.columns(values)
    groups = dict(rule.groups)
    for column in columns:
        name = rule.priority_field(column["name"])
        selected = posted.get(column["name"], column["rank"])
        column["fields"] = [form[field] for field in groups[column["name"]] if field in form.fields]
        column["field"] = form.add_prefix(name)
        auto_id = form.auto_id % column["field"] if form.auto_id else column["field"]
        column["options"] = [
            {
                "value": rank,
                "short": RANK_SHORT[rank],
                "points": points,
                "target": rule.target(column["name"], rank),
                "checked": rank == selected,
                "id": f"{auto_id}_{rank}",
            }
            for rank, points in zip(RANKS, rule.points, strict=True)
        ]
    context = {column["name"]: column for column in columns}
    context["columns"] = columns
    context["rule"] = rule.name
    return context
