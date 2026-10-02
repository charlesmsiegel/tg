"""Apply a ``CharacterTemplate`` to a character.

The template stores names and ratings; this service resolves them against the
characters app's reference data and records the application.
"""

from characters.models.core.ability_block import Ability
from characters.models.core.archetype import Archetype
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.core.specialty import Specialty
from core.models import Language, TemplateApplication


def apply_template(template, character):
    """Apply ``template`` to ``character``: set traits, create related rows, log the use."""
    # 1. Apply basic info (nature, demeanor, etc.)
    for field, value in template.basic_info.items():
        if value and isinstance(value, str) and value.startswith("FK:"):
            # Resolve foreign key: "FK:Model:Name"
            _, model_name, obj_name = value.split(":")
            if model_name == "Archetype":
                try:
                    obj = Archetype.objects.get(name=obj_name)
                    setattr(character, field, obj)
                except Archetype.DoesNotExist:
                    pass
        elif hasattr(character, field):
            setattr(character, field, value)

    # 2. Apply attributes
    for attr_name, rating in template.attributes.items():
        if hasattr(character, attr_name):
            setattr(character, attr_name, rating)

    # 3. Apply abilities
    for ability_name, rating in template.abilities.items():
        if hasattr(character, ability_name):
            setattr(character, ability_name, rating)

    # 4. Apply backgrounds
    for bg_data in template.backgrounds:
        try:
            background = Background.objects.get(name=bg_data["name"])
            BackgroundRating.objects.get_or_create(
                char=character,
                bg=background,
                defaults={"rating": bg_data.get("rating", 0)},
            )
        except Background.DoesNotExist:
            pass

    # 5. Apply powers (disciplines, spheres, gifts, etc.)
    for power_name, rating in template.powers.items():
        if hasattr(character, power_name):
            setattr(character, power_name, rating)

    # 6. Apply merits/flaws
    for mf_data in template.merits_flaws:
        try:
            merit_flaw = MeritFlaw.objects.get(name=mf_data["name"])
            MeritFlawRating.objects.get_or_create(
                character=character,
                mf=merit_flaw,
                defaults={"rating": mf_data.get("rating", 0)},
            )
        except MeritFlaw.DoesNotExist:
            pass

    # 7. Apply languages
    for lang_name in template.languages:
        try:
            language = Language.objects.get(name=lang_name)
            character.languages.add(language)
        except Language.DoesNotExist:
            pass

    # 8. Apply specialties
    for specialty_str in template.specialties:
        # Format: "Ability (Specialty)"
        if "(" in specialty_str and ")" in specialty_str:
            ability_name = specialty_str.split("(")[0].strip()
            specialty_name = specialty_str.split("(")[1].split(")")[0].strip()
            try:
                ability = Ability.objects.get(name=ability_name)
            except Ability.DoesNotExist:
                continue
            # Specialty is a shared (name, stat) row the character links to.
            specialty, _ = Specialty.objects.get_or_create(
                name=specialty_name, stat=ability.property_name
            )
            character.specialties.add(specialty)

    character.save()

    # 9. Create application record
    TemplateApplication.objects.create(character=character, template=template)

    # 10. Increment usage counter
    template.times_used += 1
    template.save(update_fields=["times_used"])
