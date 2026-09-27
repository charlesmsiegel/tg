"""Forms that enforce ``characters.rules`` point-allocation rules in ``clean()``."""

from functools import lru_cache

from django import forms

from characters.rules.allocation import first_violation


class AllocationFormMixin:
    """Validate ``allocation_rules`` (passed as a kwarg) against cleaned data.

    Only the first violation is reported, with the chargen steps' historical
    text. A violation's optional flash text is kept in ``flash_errors`` so the
    step view can repeat it as a ``messages.error`` notice.

    ``extra_clean`` is an optional callable ``(cleaned_data) -> RuleViolation |
    None`` for a check that needs the character, run after every rule passes.
    """

    def __init__(self, *args, allocation_rules=(), extra_clean=None, **kwargs):
        self.allocation_rules = tuple(allocation_rules)
        self.extra_clean = extra_clean
        self.flash_errors = []
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        violation = first_violation(self.allocation_rules, cleaned_data)
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


@lru_cache(maxsize=None)
def allocation_modelform(model, fields):
    """A ModelForm over ``fields`` (a tuple) whose clean() applies allocation rules."""
    return forms.modelform_factory(model, form=AllocationModelForm, fields=list(fields))
