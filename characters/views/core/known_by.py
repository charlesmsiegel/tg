"""The "Known by" section of reference detail pages (Spread M13, section 03).

A reference power page (a Discipline, Gift, Sphere, Lore, Merit...) lists the characters
that hold it, with their rating, grouped by chronicle. Only characters whose full sheet
the viewer may already read are listed: the viewer's own characters, every character in
a chronicle the viewer staffs (head ST, game ST or ST relationship), and every character
for staff. Chronicle-mates and observers only see a character's public card (PLAYER and
OBSERVER roles carry VIEW_PARTIAL, not VIEW_FULL), so their ratings stay hidden, and
anonymous viewers get no list at all, as on the character index.

Each reference model maps to one source describing where characters record it:

  RatingFields  an integer field on the holder models, named by the reference object
                (``Vampire.potence`` for the Potence Discipline)
  Members       a many-to-many field on the holder models (``Werewolf.gifts``)
  Ratings       a through model with a rating (``MeritFlawRating``)

Every source costs one query per holder model, whatever the number of holders.
"""

from dataclasses import dataclass
from operator import attrgetter
from typing import Callable

from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.demon.demon import Demon
from characters.models.demon.earthbound import Earthbound
from characters.models.demon.lore import Lore
from characters.models.demon.ritual import Ritual as DemonRitual
from characters.models.hunter.edge import Edge
from characters.models.hunter.hunter import Hunter
from characters.models.mage.companion import Advantage, AdvantageRating
from characters.models.mage.mage import Mage
from characters.models.mage.rote import Rote
from characters.models.mage.sorcerer import LinearMagicPath, PathRating
from characters.models.mage.sphere import Sphere
from characters.models.vampire.discipline import Discipline
from characters.models.vampire.ghoul import Ghoul
from characters.models.vampire.revenant import Revenant
from characters.models.vampire.vampire import Vampire
from characters.models.werewolf.fera import Fera
from characters.models.werewolf.garou import Werewolf
from characters.models.werewolf.gift import Gift
from characters.models.werewolf.kinfolk import Kinfolk
from characters.models.werewolf.rite import Rite
from characters.models.wraith.arcanos import Arcanos
from characters.models.wraith.thorn import Thorn
from characters.models.wraith.wraith import ThornRating, Wraith
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.cache import patch_cache_control, patch_vary_headers
from django.utils.text import slugify
from game.security import staffed_chronicles

# Rows shown at most; a staff viewer on a common Merit could otherwise pull every sheet.
KNOWN_BY_LIMIT = 100


def field_from_name(obj):
    """``False Life`` -> ``false_life``: the rating field named after the object."""
    return slugify(obj.name).replace("-", "_")


def arcanos_field(arcanos):
    """An Arcanos power is rated on its parent Arcanos' field."""
    return field_from_name(arcanos.parent_arcanos or arcanos)


def arcanos_minimum(arcanos):
    """A level-N Arcanos power is known from N dots in its Arcanos."""
    return max(arcanos.level, 1) if arcanos.parent_arcanos_id else 1


def lore_field(lore):
    """A Lore's ``property_name`` drops ``lore_of_`` / ``the_`` (see LoreBlock.lore_rows)."""
    for field in Demon._meta.concrete_fields:
        name = field.name
        if name.startswith("lore_of_") and lore.property_name in (
            name,
            name.removeprefix("lore_of_").removeprefix("the_"),
        ):
            return name
    return ""


def visible_characters(user, prefix=""):
    """Q for characters whose full sheet ``user`` can read (nobody when anonymous).

    Mirrors PermissionManager's VIEW_FULL roles: OWNER, ADMIN and the chronicle
    storyteller roles. PLAYER and OBSERVER only reach the public card.
    """
    if not user.is_authenticated:
        return Q(pk__in=[])
    q = Q(**{f"{prefix}display": True})
    if user.is_staff or user.is_superuser:
        return q
    return q & (
        Q(**{f"{prefix}owner": user})
        | Q(**{f"{prefix}chronicle__in": staffed_chronicles(user).values("pk")})
    )


def _character_related(prefix=""):
    return [f"{prefix}{name}" for name in ("owner", "chronicle", "polymorphic_ctype")]


@dataclass(frozen=True)
class RatingFields:
    """An integer rating field on each holder model, named by the reference object."""

    holders: tuple
    field: Callable = attrgetter("property_name")
    minimum: Callable = lambda obj: 1  # noqa: E731
    style: str = "dots"

    def rows(self, obj, user, limit):
        name = self.field(obj)
        if not name:
            return
        minimum = self.minimum(obj)
        for model in self.holders:
            try:
                field = model._meta.get_field(name)
            except FieldDoesNotExist:
                continue
            if not isinstance(field, models.IntegerField):
                continue
            queryset = (
                model.objects.non_polymorphic()
                .filter(visible_characters(user), **{f"{name}__gte": minimum})
                .select_related(*_character_related())
                .order_by("name")[:limit]
            )
            for character in queryset:
                yield character, getattr(character, name)


@dataclass(frozen=True)
class Members:
    """A many-to-many field on each holder model; holding it carries no rating."""

    holders: tuple
    field: str
    style: str = ""

    def rows(self, obj, user, limit):
        for model in self.holders:
            queryset = (
                model.objects.non_polymorphic()
                .filter(visible_characters(user), **{self.field: obj})
                .select_related(*_character_related())
                .order_by("name")[:limit]
            )
            for character in queryset:
                yield character, None


@dataclass(frozen=True)
class Ratings:
    """A through model: ``character`` -> ``reference`` with a non-zero ``rating``."""

    through: type
    reference: str
    character: str
    style: str = "dots"

    def rows(self, obj, user, limit):
        prefix = f"{self.character}__"
        queryset = (
            self.through.objects.filter(visible_characters(user, prefix), **{self.reference: obj})
            .exclude(rating=0)
            .select_related(*_character_related(prefix))
            .order_by(f"{prefix}name")[:limit]
        )
        for rating in queryset:
            yield getattr(rating, self.character), rating.rating


# Reference model -> where characters record it. Changeling Arts, Mummy Hekau and
# Backgrounds have no reference detail page to carry the list (Arts and Hekau are
# plain rating fields with no reference model).
KNOWN_BY_SOURCES = {
    Discipline: RatingFields((Vampire, Ghoul, Revenant)),
    Sphere: RatingFields((Mage,)),
    Lore: RatingFields((Demon, Earthbound), field=lore_field),
    Arcanos: RatingFields((Wraith,), field=arcanos_field, minimum=arcanos_minimum),
    Edge: RatingFields((Hunter,), field=field_from_name),
    Gift: Members((Werewolf, Fera, Kinfolk), "gifts"),
    Rite: Members((Werewolf, Fera), "rites_known"),
    Rote: Members((Mage,), "rotes"),
    DemonRitual: Members((Demon,), "rituals"),
    MeritFlaw: Ratings(MeritFlawRating, "mf", "character", style="number"),
    Thorn: Ratings(ThornRating, "thorn", "wraith"),
    LinearMagicPath: Ratings(PathRating, "path", "character"),
    Advantage: Ratings(AdvantageRating, "advantage", "character"),
}


def known_by_source(obj):
    for model, source in KNOWN_BY_SOURCES.items():
        if isinstance(obj, model):
            return source
    return None


def known_by(obj, user, limit=KNOWN_BY_LIMIT):
    """The Known-by list for ``obj`` as ``user`` may see it, or None.

    None means no section: the object has no holder source, or the viewer is
    anonymous. Otherwise a dict with ``groups`` (one per chronicle, each with its
    ``rows``), ``count``, ``truncated`` and the rating ``style`` (dots, number or "").
    """
    source = known_by_source(obj)
    if source is None or not user.is_authenticated:
        return None

    seen, rows = set(), []
    for character, rating in source.rows(obj, user, limit + 1):
        if character.pk in seen:
            continue
        seen.add(character.pk)
        real = character.polymorphic_ctype.model_class() or type(character)
        rows.append(
            {
                "name": character.name,
                "url": reverse("characters:character", kwargs={"pk": character.pk}),
                "type": real._meta.verbose_name.title(),
                "gameline": getattr(real, "gameline", "wod"),
                "owner": character.owner.username if character.owner else "",
                "chronicle": character.chronicle,
                "rating": rating,
                "total": max(5, rating or 0),
            }
        )

    rows.sort(
        key=lambda row: (
            row["chronicle"] is None,
            row["chronicle"].name.lower() if row["chronicle"] else "",
            row["name"].lower(),
        )
    )
    truncated = len(rows) > limit
    rows = rows[:limit]

    groups = []
    for row in rows:
        if not groups or groups[-1]["chronicle"] != row["chronicle"]:
            groups.append({"chronicle": row["chronicle"], "rows": []})
        groups[-1]["rows"].append(row)
    return {
        "groups": groups,
        "count": len(rows),
        "truncated": truncated,
        "limit": limit,
        "style": source.style,
    }


class KnownByMixin:
    """Adds ``known_by`` to a reference detail view (see characters/tl/known_by.html).

    The list depends on the viewer, and several reference detail views are wrapped in
    ``cache_page``, which keys on the URL alone. So the response always varies on the
    Cookie header (anonymous visitors, who get no list, still share cached copies),
    and a signed-in viewer's response is marked private, which ``cache_page`` never
    stores. Per-user content is therefore never written to, or served from, a
    URL-only cache entry.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["known_by"] = known_by(self.object, self.request.user)
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        patch_vary_headers(response, ("Cookie",))
        if self.request.user.is_authenticated:
            patch_cache_control(response, private=True)
        return response
