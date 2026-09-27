"""Deterministic objects for template render, query-budget and screenshot checks.

``seed()`` builds one approved instance of every concrete character, item and
location model, the reference models they point at, a chronicle and a scene
with posts. The same function backs ``scripts/template_screenshots.py`` (for
before/after screenshots) and the render and query-budget tests, so all three
look at the same pages.

Required fields are filled generically (see ``create_instance``); models that
still cannot be created are reported in ``Fixtures.skipped`` rather than
silently dropped.
"""

import re
from dataclasses import dataclass, field
from datetime import date

from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models, transaction

FIXTURE_APPS = ("characters", "items", "locations", "core", "game")
RATING_FIELDS = {
    "strength": 3,
    "dexterity": 2,
    "wits": 4,
    "alertness": 2,
    "athletics": 3,
    "brawl": 1,
    "firearms": 4,
    "occult": 4,
    "willpower": 5,
}
# Reference rows whose ``property_name`` names a character field.
PROPERTY_NAMES = {"Sphere": "forces", "Ability": "alertness", "Background": "contacts"}
SKIP_MODELS = {
    # Join/through and bookkeeping rows with no page of their own.
    "core.Model",
}


@dataclass
class Fixtures:
    st: User
    player: User
    chronicle: object
    scene: object
    objects: dict = field(default_factory=dict)  # model label -> instance
    skipped: dict = field(default_factory=dict)  # model label -> reason


def _placeholder(model_field, label):
    if isinstance(model_field, models.EmailField):
        return "fixture@example.com"
    if isinstance(model_field, models.URLField):
        return "https://example.com/"
    if isinstance(model_field, models.CharField | models.TextField):
        if model_field.choices:
            return model_field.choices[0][0]
        return f"Fixture {label}"[: model_field.max_length or 200]
    if isinstance(model_field, models.BooleanField):
        return False
    if isinstance(model_field, models.DateTimeField | models.DateField):
        return date(2024, 1, 1)
    if isinstance(model_field, models.IntegerField | models.FloatField | models.DecimalField):
        return model_field.choices[0][0] if model_field.choices else 1
    if isinstance(model_field, models.JSONField):
        return {}
    return None


def create_instance(model, cache, **overrides):
    """Create ``model`` filling every required field; related rows come from ``cache``."""
    values = {}
    for model_field in model._meta.concrete_fields:
        name = model_field.name
        if name in overrides or model_field.primary_key or model_field.auto_created:
            continue
        if isinstance(model_field, models.OneToOneField) and model_field.remote_field.parent_link:
            continue
        if model_field.null or model_field.blank:
            continue
        if model_field.has_default() and model_field.get_default() not in ("", None):
            continue
        if model_field.is_relation:
            related = model_field.related_model
            if related is model:
                continue
            values[name] = related_instance(related, cache)
            continue
        if name == "property_name":
            values[name] = PROPERTY_NAMES.get(model.__name__, "strength")
            continue
        value = _placeholder(model_field, model.__name__)
        if value is not None:
            values[name] = value
    if any(f.name == "name" for f in model._meta.concrete_fields):
        values.setdefault("name", f"Fixture {model.__name__}")
    values.update(overrides)
    with transaction.atomic():
        return model.objects.create(**values)


def related_instance(model, cache):
    label = model._meta.label
    if label not in cache:
        if model is User:
            cache[label] = User.objects.first()
        else:
            existing = model._default_manager.first()
            cache[label] = existing or create_instance(concrete_leaf(model), cache)
    return cache[label]


def concrete_leaf(model):
    if not model._meta.abstract:
        return model
    for sub in model.__subclasses__():
        return concrete_leaf(sub)
    return model


def _field_names(model):
    return {f.name for f in model._meta.get_fields()}


def _object_models():
    from characters.models.core import CharacterModel
    from items.models.core import ItemModel
    from locations.models.core import LocationModel

    trees = (CharacterModel, ItemModel, LocationModel)
    found = []
    for app in FIXTURE_APPS:
        for model in apps.get_app_config(app).get_models():
            if model._meta.abstract or model._meta.proxy:
                continue
            if model._meta.label in SKIP_MODELS:
                continue
            if issubclass(model, trees) or hasattr(model, "get_absolute_url"):
                found.append(model)
    return sorted(found, key=lambda m: m._meta.label)


def seed():
    """Create the fixture set in the current database and return it."""
    from accounts.models import Profile  # noqa: F401  (profile signal)
    from characters.models.core import CharacterModel
    from characters.models.core.specialty import Specialty
    from game.models import Chronicle, Gameline, Post, Scene, STRelationship
    from items.models.core import ItemModel
    from locations.models.core import LocationModel

    st = User.objects.create_superuser("fixture_st", "st@example.com", "fixture-pass")
    player = User.objects.create_user("fixture_player", "player@example.com", "fixture-pass")
    chronicle = Chronicle.objects.create(name="Fixture Chronicle", head_st=st)
    gameline = Gameline.objects.create(name="Fixture Gameline")
    STRelationship.objects.create(user=st, chronicle=chronicle, gameline=gameline)
    cache = {"auth.User": st, "game.Chronicle": chronicle}
    fixtures = Fixtures(st=st, player=player, chronicle=chronicle, scene=None)
    alertness = Specialty.objects.create(name="Keen Ears", stat="alertness")
    strength = Specialty.objects.create(name="Iron Grip", stat="strength")

    for model in _object_models():
        label = model._meta.label
        overrides = {}
        names = _field_names(model)
        if issubclass(model, CharacterModel | ItemModel | LocationModel):
            overrides.update(owner=player, status="App")
            if "chronicle" in names:
                overrides["chronicle"] = chronicle
        if "parent_practice" in names:
            # The Mage XP form assumes every specialized practice has a parent.
            overrides["parent_practice"] = related_instance(
                apps.get_model("characters", "Practice"), cache
            )
        if issubclass(model, CharacterModel):
            overrides.update(
                {k: v for k, v in RATING_FIELDS.items() if k in names},
                concept="Fixture concept",
            )
        try:
            instance = create_instance(model, cache, **overrides)
        except (IntegrityError, TypeError, ValueError, AttributeError, ValidationError) as exc:
            fixtures.skipped[label] = f"{type(exc).__name__}: {exc}"
            continue
        if "specialties" in names and hasattr(instance, "specialties"):
            instance.specialties.add(alertness, strength)
        fixtures.objects[label] = instance
        cache.setdefault(label, instance)

    location = fixtures.objects.get("locations.LocationModel") or LocationModel.objects.first()
    scene = Scene.objects.create(name="Fixture Scene", chronicle=chronicle, location=location)
    character = next(
        obj for label, obj in sorted(fixtures.objects.items()) if isinstance(obj, CharacterModel)
    )
    scene.characters.add(character)
    st_character = next(
        obj
        for label, obj in sorted(fixtures.objects.items())
        if isinstance(obj, CharacterModel) and obj is not character
    )
    st_character.owner = st
    st_character.save()
    scene.characters.add(st_character)
    for number, author in enumerate([character, st_character] * 3):
        Post.objects.create(
            scene=scene,
            character=author,
            display_name=f"{author.name} {number}",
            message=f"Fixture post {number}",
        )
    fixtures.scene = scene
    return fixtures


def _slug(*parts):
    return re.sub(r"[^A-Za-z0-9]+", "_", "_".join(parts)).strip("_")


def list_urls():
    """Every routed list/index page of the object apps that takes no arguments."""
    from django.urls import URLPattern, URLResolver, get_resolver, reverse
    from django.urls.exceptions import NoReverseMatch

    def walk(patterns, namespaces=()):
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                scope = namespaces + ((pattern.namespace,) if pattern.namespace else ())
                yield from walk(pattern.url_patterns, scope)
            elif isinstance(pattern, URLPattern) and pattern.name:
                name = ":".join((*namespaces, pattern.name))
                if namespaces and namespaces[0] in {"characters", "items", "locations", "game"}:
                    if "list" in name.split(":") or pattern.name in {"index", "chronicles"}:
                        yield name

    urls = {}
    for name in sorted(set(walk(get_resolver().url_patterns))):
        try:
            urls[name] = reverse(name)
        except NoReverseMatch:
            continue
    return urls


def fixture_pages(fixtures):
    """{slug: url} for every fixture detail/edit page, list page, the index and the scene."""
    pages = {}
    for label, obj in sorted(fixtures.objects.items()):
        for kind, method in (("detail", "get_absolute_url"), ("edit", "get_update_url")):
            try:
                url = getattr(obj, method)()
            except Exception:  # noqa: BLE001 - a model without that URL has no such page
                continue
            pages[_slug(label, kind)] = url
    pages.update({_slug("list", name): url for name, url in list_urls().items()})
    pages["scene_detail"] = fixtures.scene.get_absolute_url()
    pages["characters_index"] = "/characters/index/"
    return pages
