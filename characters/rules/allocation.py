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


def label(name: str) -> str:
    """Display name for a rule or group; the live hints and feedback both use it."""
    return name.replace("_", " ").title()


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

    def satisfied(self, values: Mapping[str, int | None]) -> bool:
        current = self.current(values)
        return current <= self.total if self.comparison == "at_most" else current == self.total

    def status(self, values: Mapping[str, int | None]) -> dict:
        """Running total for display; the form's violations remain the verdict."""
        return {
            "name": self.name,
            "label": label(self.name),
            "current": self.current(values),
            "target": self.total,
            "comparison": self.comparison,
            "satisfied": self.satisfied(values),
        }

    def client_data(self) -> dict:
        data = {
            "name": self.name,
            "label": label(self.name),
            "total": self.total,
            "comparison": self.comparison,
            "fields": list(self.fields),
        }
        if self.maximum is not None:
            data["max"] = self.maximum
        return data


RANKS = ("primary", "secondary", "tertiary")
RANK_SHORT = {"primary": "Pri", "secondary": "Sec", "tertiary": "Ter"}


@dataclass(frozen=True)
class PriorityRule:
    """Groups ranked primary/secondary/tertiary, each totalling its rank's points.

    ``base`` is the free rating every field starts with (1 for Attributes), so
    a group of three Attributes must total ``3 * base + points``. Every rated
    field must lie within ``minimum``..``maximum``; that range check runs
    before the distribution check, as the chargen views always did.

    The player ranks the groups with one choice per group (``priority_field``,
    posted as ``primary``/``secondary``/``tertiary``). When no choice is posted
    the ranking is inferred from the dots: the group totals, sorted, must equal
    the targets in any order. A partial or repeated choice is an error.

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
    ranks_message: str = "Choose primary, secondary and tertiary once each for {groups}"

    @property
    def fields(self) -> tuple[str, ...]:
        if self.range_fields is not None:
            return self.range_fields
        return tuple(name for _, names in self.groups for name in names)

    @staticmethod
    def priority_field(group: str) -> str:
        """The form field holding a group's chosen rank."""
        return f"priority_{group}"

    @property
    def priority_fields(self) -> tuple[str, ...]:
        return tuple(self.priority_field(group) for group, _ in self.groups)

    def group_totals(self, values: Mapping[str, int | None]) -> dict[str, int]:
        return {group: sum(_value(values, name) for name in names) for group, names in self.groups}

    def target(self, group: str, rank: str) -> int:
        """What ``group`` must total when it holds ``rank``."""
        names = dict(self.groups)[group]
        return self.base * len(names) + self.points[RANKS.index(rank)]

    def _targets(self) -> list[int]:
        primary, secondary, tertiary = self.points
        return sorted(
            self.base * len(names) + points
            for (_, names), points in zip(self.groups, (tertiary, secondary, primary), strict=False)
        )

    def posted_ranks(self, values: Mapping) -> dict[str, str]:
        """The ranks a submission chose, by group (groups without a choice are left out)."""
        posted = {}
        for group, _ in self.groups:
            rank = values.get(self.priority_field(group))
            if rank in RANKS:
                posted[group] = rank
        return posted

    def chosen_ranks(self, values: Mapping) -> dict[str, str] | None:
        """The posted ranking when every group holds a different rank, else None."""
        posted = self.posted_ranks(values)
        if len(posted) == len(self.groups) and len(set(posted.values())) == len(posted):
            return posted
        return None

    def rank_conflict(self, values: Mapping) -> bool:
        """A choice was posted but it does not rank every group exactly once."""
        return bool(self.posted_ranks(values)) and self.chosen_ranks(values) is None

    def inferred_ranks(self, values: Mapping) -> dict[str, str]:
        """Ranks by current totals, largest first; ties keep the groups' order."""
        totals = self.group_totals(values)
        order = sorted(self.groups, key=lambda group: -totals[group[0]])
        return {group: rank for (group, _), rank in zip(order, RANKS, strict=False)}

    def ranks(self, values: Mapping) -> tuple[dict[str, str], bool]:
        """``(ranks, chosen)``: the posted ranking if complete, else the inferred one."""
        chosen = self.chosen_ranks(values)
        if chosen is not None:
            return chosen, True
        return self.inferred_ranks(values), False

    def _ranked_summary(self, ranks: Mapping[str, str]) -> str:
        return ", ".join(f"{label(group)} {ranks[group]}" for group, _ in self.groups)

    def violations(self, values: Mapping[str, int | None], phase: str) -> list[RuleViolation]:
        if phase != TOTALS:
            return []
        if any(not self.minimum <= _value(values, name) <= self.maximum for name in self.fields):
            return [RuleViolation(self.range_message, flash=self.range_flash)]
        if self.rank_conflict(values):
            names = [label(group) for group, _ in self.groups]
            groups = ", ".join(names[:-1]) + " and " + names[-1]
            return [RuleViolation(self.ranks_message.format(groups=groups))]
        totals = self.group_totals(values)
        chosen = self.chosen_ranks(values)
        if chosen is not None:
            broken = any(totals[group] != self.target(group, chosen[group]) for group in totals)
        else:
            broken = sorted(totals.values()) != self._targets()
        if broken:
            primary, secondary, tertiary = self.points
            message = self.message.format(primary=primary, secondary=secondary, tertiary=tertiary)
            if chosen is not None:
                message = f"{message} as ranked ({self._ranked_summary(chosen)})"
            flash = None
            if self.flash:
                flash = self.flash.format(allocation=message, **totals)
            return [RuleViolation(message, flash=flash)]
        return []

    def targets(self) -> list[int]:
        """Group totals a valid allocation has, largest first."""
        return sorted(self._targets(), reverse=True)

    def columns(self, values: Mapping) -> list[dict]:
        """Per-group running counts against the ranking in force (chosen or inferred).

        Each column: ``name``, ``label``, ``rank``, ``target``, ``current``,
        ``left`` (negative when over), ``state`` (``progress``/``done``/``over``)
        and ``count`` ("2 left", "done", "1 over").
        """
        totals = self.group_totals(values)
        ranks, _ = self.ranks(values)
        columns = []
        for group, _ in self.groups:
            target = self.target(group, ranks[group])
            left = target - totals[group]
            if left > 0:
                state, count = "progress", f"{left} left"
            elif left < 0:
                state, count = "over", f"{-left} over"
            else:
                state, count = "done", "done"
            columns.append(
                {
                    "name": group,
                    "label": label(group),
                    "rank": ranks[group],
                    "target": target,
                    "current": totals[group],
                    "left": left,
                    "state": state,
                    "count": count,
                }
            )
        return columns

    def status(self, values: Mapping[str, int | None]) -> dict:
        """Running group totals for display; the form's violations remain the verdict.

        When the submission chose a ranking, each group also carries its
        ``rank``, ``target`` and ``count`` and the status is ``ranked``.
        """
        totals = self.group_totals(values)
        chosen = self.chosen_ranks(values)
        groups = [
            {"name": group, "label": label(group), "current": totals[group]}
            for group, _ in self.groups
        ]
        if chosen is not None:
            for group, column in zip(groups, self.columns(values), strict=True):
                group.update(
                    rank=column["rank"],
                    target=column["target"],
                    count=column["count"],
                    state=column["state"],
                )
            satisfied = all(group["current"] == group["target"] for group in groups)
        else:
            satisfied = sorted(totals.values()) == self._targets()
        return {
            "name": self.name,
            "label": label(self.name),
            "groups": groups,
            "targets": self.targets(),
            "ranked": chosen is not None,
            "satisfied": satisfied,
        }

    def client_data(self) -> dict:
        primary, secondary, tertiary = self.points
        return {
            "name": self.name,
            "primary": primary,
            "secondary": secondary,
            "tertiary": tertiary,
            "min": self.minimum,
            "max": self.maximum,
            "base": self.base,
            "groups": [[group, list(names)] for group, names in self.groups],
            "group_labels": {group: label(group) for group, _ in self.groups},
            "targets": self.targets(),
            "priority_fields": {group: self.priority_field(group) for group, _ in self.groups},
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
