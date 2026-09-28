"""Group a character create / edit form's fields into Spread sections.

    {% load character_edit %}
    {% character_edit_sections form as sections %}

Used by characters/tl/character_edit_fields.html. The grouping follows the widgets, so
the same template serves a Storyteller's full form and an owner's limited form
(LimitedHumanEditForm): every field the form carries is rendered exactly once.
"""

from django import forms, template

register = template.Library()

ATTRIBUTE_COLUMNS = (
    ("Physical", ("strength", "dexterity", "stamina")),
    ("Social", ("charisma", "manipulation", "appearance")),
    ("Mental", ("perception", "intelligence", "wits")),
)
ABILITY_GROUPS = (("Talents", "talents"), ("Skills", "skills"), ("Knowledges", "knowledges"))


def field_kind(bound_field):
    """hidden, check, long (textareas, multi-selects), rating (numbers) or field."""
    widget = bound_field.field.widget
    if bound_field.is_hidden:
        return "hidden"
    if isinstance(widget, forms.CheckboxInput):
        return "check"
    if isinstance(widget, (forms.Textarea, forms.SelectMultiple, forms.CheckboxSelectMultiple)):
        return "long"
    if isinstance(widget, forms.NumberInput):
        return "rating"
    return "field"


def _columns(form, groups, ratings):
    """[(title, [bound fields])] for the named rating fields present in the form."""
    columns = []
    for title, names in groups:
        fields = [form[name] for name in names if name in ratings]
        if fields:
            columns.append((title, fields))
            for name in names:
                ratings.pop(name, None)
    return columns


def _split(fields, count=3):
    """Spread fields over up to ``count`` columns, filling each column in turn."""
    size = -(-len(fields) // count) if fields else 0
    return [("", fields[i : i + size]) for i in range(0, len(fields), size)] if size else []


@register.simple_tag
def character_edit_sections(form):
    """Hidden fields plus numbered sections, in the order the page shows them.

    Each section is a dict: ``title``, ``kind`` ("grid", "columns" or "long"),
    ``fields`` (grid / long) or ``columns`` (a list of ``(title, fields)``).
    """
    instance = getattr(form, "instance", None)
    hidden, grid, tail, long_fields = [], [], [], []
    ratings = {}
    for bound_field in form:
        kind = field_kind(bound_field)
        if kind == "hidden":
            hidden.append(bound_field)
        elif kind == "long":
            long_fields.append(bound_field)
        elif kind == "rating":
            ratings[bound_field.name] = bound_field
        elif kind == "check" or bound_field.widget_type in ("file", "clearablefile"):
            tail.append(bound_field)  # image upload and checkboxes close the grid
        else:
            grid.append(bound_field)
    grid += tail

    attributes = _columns(form, ATTRIBUTE_COLUMNS, ratings)
    ability_groups = [
        (title, tuple(getattr(instance, attr, None) or ())) for title, attr in ABILITY_GROUPS
    ]
    abilities = _columns(form, ability_groups, ratings)
    others = _split(list(ratings.values()))

    sections = []
    if grid:
        sections.append({"title": "Identity", "kind": "grid", "fields": grid})
    if attributes:
        sections.append({"title": "Attributes", "kind": "columns", "columns": attributes})
    if abilities:
        sections.append({"title": "Abilities", "kind": "columns", "columns": abilities})
    if others:
        sections.append({"title": "Traits", "kind": "columns", "columns": others})
    if long_fields:
        sections.append({"title": "Details", "kind": "long", "fields": long_fields})
    for number, section in enumerate(sections, start=1):
        section["num"] = f"{number:02d}"
    return {"hidden": hidden, "sections": sections}
