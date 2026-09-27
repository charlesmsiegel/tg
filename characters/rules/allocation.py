"""Pure point-allocation rules shared by forms, views and client-side hints.

A rule knows which submitted fields it constrains and returns the violations of
a mapping of field name to rating. Rules never touch the database, so they are
unit-testable without fixtures and can be serialized for the browser with
``client_data()``.

Forms evaluate rules in phases so that the first error reported matches the
order the chargen views have always used: every total first, then per-trait
bounds, then restricted-choice checks.
"""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field

TOTALS = "totals"
BOUNDS = "bounds"
CHOICES = "choices"
PHASES = (TOTALS, BOUNDS, CHOICES)


@dataclass(frozen=True)
class RuleViolation:
    """One broken rule: a form error plus an optional extra flash message."""

    message: str
    field: str | None = None
    flash: str | None = None


def _value(values: Mapping[str, int | None], name: str) -> int:
    return values.get(name) or 0


@dataclass(frozen=True)
class AllocationRule:
    """Fields that must sum to exactly (or at most) ``total``.

    ``maximum`` bounds each trait; ``allowed`` restricts which traits may be
    rated above zero (for example in-clan Disciplines). Message templates are
    formatted with ``total``, ``current`` and, for per-field messages,
    ``label`` (the field name in title case).
    """

    name: str
    fields: tuple[str, ...]
    total: int
    message: str
    comparison: str = "exact"
    flash: str | None = None
    maximum: int | None = None
    maximum_message: str = "Cannot exceed {maximum} dots"
    maximum_flash: str | None = None
    allowed: frozenset[str] | None = None
    allowed_message: str = ""
    allowed_flash: str | None = None

    def current(self, values: Mapping[str, int | None]) -> int:
        return sum(_value(values, name) for name in self.fields)

    def _format(self, template, values, name=None):
        if template is None:
            return None
        return template.format(
            total=self.total,
            current=self.current(values),
            maximum=self.maximum,
            label=(name or "").replace("_", " ").title(),
        )

    def violations(self, values: Mapping[str, int | None], phase: str) -> list[RuleViolation]:
        if phase == TOTALS:
            current = self.current(values)
            broken = current > self.total if self.comparison == "at_most" else current != self.total
            if broken:
                return [
                    RuleViolation(
                        self._format(self.message, values), flash=self._format(self.flash, values)
                    )
                ]
        elif phase == BOUNDS and self.maximum is not None:
            return [
                RuleViolation(
                    self._format(self.maximum_message, values, name),
                    field=name,
                    flash=self._format(self.maximum_flash, values, name),
                )
                for name in self.fields
                if _value(values, name) > self.maximum
            ]
        elif phase == CHOICES and self.allowed is not None:
            return [
                RuleViolation(
                    self._format(self.allowed_message, values, name),
                    field=name,
                    flash=self._format(self.allowed_flash, values, name),
                )
                for name in self.fields
                if _value(values, name) > 0 and name not in self.allowed
            ]
        return []

    def client_data(self) -> dict[str, int | str]:
        data = {"name": self.name, "total": self.total, "comparison": self.comparison}
        if self.maximum is not None:
            data["max"] = self.maximum
        return data


@dataclass(frozen=True)
class PriorityRule:
    """Groups whose totals, sorted, equal primary/secondary/tertiary points.

    ``base`` is the free rating every field starts with (1 for Attributes), so
    a group of three Attributes must total ``3 * base + points``. Every rated
    field must lie within ``minimum``..``maximum``; that range check runs
    before the distribution check, as the chargen views always did.
    ``message`` is formatted with ``primary``, ``secondary`` and ``tertiary``;
    ``flash`` additionally with ``allocation`` (the formatted message) and each
    group's name mapped to its current total.
    """

    name: str
    groups: tuple[tuple[str, tuple[str, ...]], ...]
    points: tuple[int, int, int]
    message: str
    range_message: str
    minimum: int = 0
    maximum: int = 5
    base: int = 0
    flash: str | None = None
    range_flash: str | None = None
    range_fields: tuple[str, ...] | None = field(default=None)

    @property
    def fields(self) -> tuple[str, ...]:
        if self.range_fields is not None:
            return self.range_fields
        return tuple(name for _, names in self.groups for name in names)

    def group_totals(self, values: Mapping[str, int | None]) -> dict[str, int]:
        return {group: sum(_value(values, name) for name in names) for group, names in self.groups}

    def _targets(self) -> list[int]:
        primary, secondary, tertiary = self.points
        return sorted(
            self.base * len(names) + points
            for (_, names), points in zip(self.groups, (tertiary, secondary, primary), strict=False)
        )

    def violations(self, values: Mapping[str, int | None], phase: str) -> list[RuleViolation]:
        if phase != TOTALS:
            return []
        if any(not self.minimum <= _value(values, name) <= self.maximum for name in self.fields):
            return [RuleViolation(self.range_message, flash=self.range_flash)]
        totals = self.group_totals(values)
        if sorted(totals.values()) != self._targets():
            primary, secondary, tertiary = self.points
            message = self.message.format(primary=primary, secondary=secondary, tertiary=tertiary)
            flash = None
            if self.flash:
                flash = self.flash.format(allocation=message, **totals)
            return [RuleViolation(message, flash=flash)]
        return []

    def client_data(self) -> dict[str, int | str]:
        primary, secondary, tertiary = self.points
        return {
            "name": self.name,
            "primary": primary,
            "secondary": secondary,
            "tertiary": tertiary,
            "min": self.minimum,
            "max": self.maximum,
            "base": self.base,
        }


def first_violation(rules: Iterable, values: Mapping[str, int | None]) -> RuleViolation | None:
    """The violation a chargen step reports: earliest phase, then rule order."""
    rules = list(rules)
    for phase in PHASES:
        for rule in rules:
            found = rule.violations(values, phase)
            if found:
                return found[0]
    return None
