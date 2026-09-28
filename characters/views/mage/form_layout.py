"""Section layout for the Mage-family create / edit forms (Mage, MtA Human, Companion, Sorcerer).

``characters/mage/form/sections.html`` renders ``form_sections``: numbered sections of
fields, or of trait columns (Attributes, Abilities, Spheres) as label + number rows.
The layout is declared per view; a field the layout does not place still renders, in a
closing "Other" section, so a POST never fails on a field the page left out. Fields the
bound form lacks (an owner's limited form) are skipped and empty sections dropped.
"""

ATTRIBUTES = "attributes"
ABILITIES = "abilities"
SECONDARY_ABILITIES = "secondary_abilities"
SPHERES = "spheres"

ATTRIBUTE_COLUMNS = (
    ("Physical", ("strength", "dexterity", "stamina")),
    ("Social", ("charisma", "manipulation", "appearance")),
    ("Mental", ("perception", "intelligence", "wits")),
)
# Sheet order (spheres/tl_grid.html), read down each column.
SPHERE_COLUMNS = (
    ("correspondence", "entropy", "forces"),
    ("life", "matter", "mind"),
    ("prime", "spirit", "time"),
)
SPHERE_NAME_FIELDS = {"correspondence": "corr_name", "prime": "prime_name", "spirit": "spirit_name"}

BIOGRAPHY = (
    "date_of_birth",
    "age",
    "apparent_age",
    "age_of_awakening",
    "description",
)
STORY = ("history", "avatar_description", "goals", "public_info", "notes", "st_notes")
TRAITS = ("specialties", "derangements", "merits_and_flaws")
# Labels the verbose names get wrong ("Npc", "Xp", "St notes").
FIELD_LABELS = {"npc": "NPC", "xp": "XP", "st_notes": "ST notes"}
IDENTITY = ("name", "owner", "chronicle", "concept", "nature", "demeanor", "npc")

MTA_HUMAN_LAYOUT = (
    ("Identity", IDENTITY + ("image",)),
    ("Attributes", ATTRIBUTES),
    ("Abilities", ABILITIES),
    ("Secondary abilities", SECONDARY_ABILITIES, {"reveal": True}),
    ("Advantages", ("willpower",)),
    ("Traits", TRAITS),
    ("Biography", BIOGRAPHY),
    ("Story", STORY),
)
MAGE_LAYOUT = (
    ("Identity", IDENTITY + ("essence", "affiliation", "faction", "subfaction", "image")),
    ("Attributes", ATTRIBUTES),
    ("Abilities", ABILITIES),
    ("Secondary abilities", SECONDARY_ABILITIES, {"reveal": True}),
    ("Spheres", SPHERES, {"power": True}),
    (
        "Magick",
        (
            "arete",
            "affinity_sphere",
            "corr_name",
            "prime_name",
            "spirit_name",
            "quintessence",
            "paradox",
            "rote_points",
        ),
        {"power": True},
    ),
    ("Advantages", ("willpower", "quiet", "quiet_type")),
    ("Traits", TRAITS),
    ("Biography", BIOGRAPHY),
    ("Story", STORY),
)
SORCERER_LAYOUT = (
    ("Identity", IDENTITY + ("status", "image")),
    (
        "Sorcery",
        (
            "sorcerer_type",
            "fellowship",
            "affinity_path",
            "casting_attribute",
            "quintessence",
            "willpower",
        ),
        {"power": True},
    ),
    ("Attributes", ATTRIBUTES),
    ("Abilities", ABILITIES),
    ("Secondary abilities", SECONDARY_ABILITIES, {"reveal": True}),
    ("Traits", TRAITS),
    ("Biography", BIOGRAPHY),
    ("Story", STORY),
)
COMPANION_LAYOUT = (
    ("Identity", IDENTITY + ("companion_type", "companion_of", "image")),
    ("Advantages", ("willpower",)),
    ("Biography", BIOGRAPHY),
    ("Story", STORY),
    ("Storyteller", ("status", "xp", "freebies_approved", "display", "visibility")),
)


class MageFamilyFormMixin:
    """Add ``form_sections`` for the view's ``form_layout`` to the context.

    ``form_layout`` is a sequence of ``(title, spec)`` or ``(title, spec, options)``;
    ``spec`` is a tuple of field names or one of ATTRIBUTES / ABILITIES /
    SECONDARY_ABILITIES / SPHERES, ``options`` a dict (``power``: accent the section,
    ``reveal``: collapse it behind a button, ``note``: a line under the heading).
    """

    form_layout = ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_sections"] = build_form_sections(
            context["form"], self.model, getattr(self, "object", None), self.form_layout
        )
        return context


def build_form_sections(form, model, character, layout):
    for name, label in FIELD_LABELS.items():
        if name in form.fields:
            form.fields[name].label = label
    used = set()
    sections = []

    def take(name):
        if name in form.fields and name not in used and not form[name].is_hidden:
            used.add(name)
            return form[name]
        return None

    def field_label(name):
        return form[name].label

    def column(heading, names, label=field_label):
        """``(heading, [(bound field, label), ...])`` for the names the form has."""
        rows = []
        for name in names:
            field = take(name)
            if field is not None:
                rows.append((field, label(name)))
        return heading, rows

    def ability_label(stat):
        text = model.ability_label(stat)
        specialty = character.get_specialty(stat) if character is not None else None
        return f"{text} ({specialty})" if specialty else text

    def sphere_label(name):
        # The name the mage uses (Data, Primal Utility, Dimensional Science...).
        name_field = SPHERE_NAME_FIELDS.get(name)
        if name_field and character is not None:
            return getattr(character, f"get_{name_field}_display")()
        return name.title()

    for entry in layout:
        title, spec, options = (*entry, {}) if len(entry) == 2 else entry
        if spec == ATTRIBUTES:
            columns = [column(heading, names) for heading, names in ATTRIBUTE_COLUMNS]
        elif spec in (ABILITIES, SECONDARY_ABILITIES):
            primary = spec == ABILITIES
            columns = []
            for heading, group in model.ABILITY_GROUPS:
                stats = [
                    stat
                    for stat in getattr(model, group)
                    if (stat in model.primary_abilities) == primary
                ]
                stats.sort(key=model.ability_label)
                columns.append(column(heading, stats, ability_label))
        elif spec == SPHERES:
            columns = [column("", names, sphere_label) for names in SPHERE_COLUMNS]
        else:
            fields = [f for f in (take(name) for name in spec) if f is not None]
            if fields:
                sections.append({"title": title, "fields": fields, **options})
            continue
        if any(rows for _heading, rows in columns):
            sections.append({"title": title, "columns": columns, **options})

    others = [form[name] for name in form.fields if name not in used and not form[name].is_hidden]
    if others:
        sections.append({"title": "Other", "fields": others})
    for number, section in enumerate(sections, start=1):
        section["num"] = f"{number:02d}"
        # A collapsed section opens when one of its fields has an error.
        section["open"] = any(field.errors for field in section_fields(section))
    return sections


def section_fields(section):
    if "fields" in section:
        return section["fields"]
    return [field for _heading, rows in section["columns"] for field, _label in rows]
