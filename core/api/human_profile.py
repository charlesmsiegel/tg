"""Explicit exposed Human profile, not a full archive or local Store mapping."""

import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.crypto import salted_hmac
from rest_framework.exceptions import APIException

from core.api.projections import ABILITIES, ATTRIBUTES
from core.constants import CharacterStatus

PROFILE = "tg-human-v1"
RELATION_LIMIT = 500
CAPABILITIES = {
    "read": True,
    "create": False,
    "update": False,
    "delete": False,
    "compare_and_swap": False,
}
REDACTIONS = (
    "st_notes",
    "image",
    "image_status",
    "spent_freebies",
    "freebie_spendings",
    "xp_spending_history",
    "reverse_memberships",
    "pooled_group_data",
)
SCALARS = (
    "type",
    "gameline",
    "name",
    "owner_id",
    "chronicle_id",
    "status",
    "npc",
    "display",
    "visibility",
    "concept",
    "notes",
    "description",
    "public_info",
    "creation_status",
    "freebies_approved",
    "nature_id",
    "demeanor_id",
    "willpower",
    "temporary_willpower",
    "age",
    "apparent_age",
    "date_of_birth",
    "history",
    "goals",
    "xp",
    "freebies",
    "current_health_levels",
    "max_health_levels",
)
SCALAR_IDS = {"owner_id", "chronicle_id", "nature_id", "demeanor_id"}
RELATIONS = {
    "backgrounds": (
        "backgrounds",
        ("id", "bg_id", "rating", "note", "url", "complete", "pooled", "display_alt_name"),
    ),
    "merits_flaws": ("merit_flaw_ratings", ("id", "mf_id", "rating")),
    "specialties": ("specialties", ("id",)),
    "languages": ("languages", ("id",)),
    "derangements": ("derangements", ("id",)),
    "sources": ("sources", ("id", "book_id", "page")),
}
RELATION_IDS = {"id", "bg_id", "mf_id", "book_id"}
CATALOG_FIELDS = {
    "archetypes": ("id", "name"),
    "backgrounds": ("id", "name", "property_name", "multiplier", "alternate_name", "poolable"),
    "merits-flaws": ("id", "name", "min_rating", "max_rating"),
    "specialties": ("id", "name", "stat"),
    "languages": ("id", "name", "frequency"),
    "derangements": ("id", "name"),
    "books": ("id", "name", "url", "edition", "gameline", "storytellers_vault"),
}


class ProfileError(APIException):
    status_code = 422

    def __init__(self, error, field=None, status=422):
        self.status_code = status
        super().__init__({"error": error} | ({"field": field} if field else {}))


def native_id(value):
    return None if value is None else str(value)


def manifest():
    return {
        "profile": PROFILE,
        "archive_complete": False,
        "concrete_types": ["human"],
        "id_encoding": "decimal-string",
        "identity_namespace": "configured-origin/resource-kind/native-id",
        "character_fields": [*SCALARS, "attributes", "abilities", "wound_penalty"],
        "attributes": list(ATTRIBUTES),
        "abilities": list(ABILITIES),
        "relations": {key: list(fields) for key, (_name, fields) in RELATIONS.items()},
        "catalogs": {
            key: [*fields, *(["ratings", "allowed_types"] if key == "merits-flaws" else [])]
            for key, fields in CATALOG_FIELDS.items()
        },
        "catalog_relations": {
            "merits-flaws": {
                "ratings": {"type": "integer-array", "maximum_items": RELATION_LIMIT},
                "allowed_types": {
                    "fields": ["id", "name", "type", "gameline"],
                    "id_encoding": "decimal-string",
                    "maximum_items": RELATION_LIMIT,
                },
            }
        },
        "bounds": {
            "attributes": {"min": 0, "max": 10},
            "abilities": {"min": 0, "max": 10},
            "willpower": {"min": 1, "max": 10},
            "temporary_willpower": {"min": 0, "max": 10, "at_most": "willpower"},
            "age": {"min": 0, "max": 65535, "nullable": True},
            "background_rating": {"min": 0, "max": 10},
            "merit_flaw_rating": {"min": -10, "max": 10},
        },
        "statuses": [value for value, _label in CharacterStatus.CHOICES],
        "relation_limit": RELATION_LIMIT,
        "pagination": {"default": 50, "maximum": 100},
        "redactions": list(REDACTIONS),
        "capabilities": dict(CAPABILITIES),
        "snapshot_scope": "exposed profile and relation identities; not a CAS or permission lease",
    }


def human_projection(human):
    fields = {
        key: native_id(getattr(human, key)) if key in SCALAR_IDS else getattr(human, key)
        for key in SCALARS
    }
    fields["attributes"] = {key: getattr(human, key) for key in ATTRIBUTES}
    fields["abilities"] = {key: getattr(human, key) for key in ABILITIES}
    fields["wound_penalty"] = human.get_wound_penalty()
    relations = {}
    for key, (name, selected) in RELATIONS.items():
        rows = list(getattr(human, name).order_by("pk").values(*selected)[: RELATION_LIMIT + 1])
        if len(rows) > RELATION_LIMIT:
            raise ProfileError("profile_limit", key)
        relations[key] = [
            {
                column: native_id(value) if column in RELATION_IDS else value
                for column, value in row.items()
            }
            for row in rows
        ]
    return {
        "profile": PROFILE,
        "complete": False,
        "identity": {"kind": "character", "id": native_id(human.pk)},
        "character": fields,
        "relations": relations,
        "redactions": list(REDACTIONS),
        "capabilities": dict(CAPABILITIES),
    }


def fingerprint(request, data):
    scope = {
        "principal": str(request.user.pk),
        "origin": f"{request.scheme}://{request.get_host().lower()}",
        "script_prefix": request.META.get("SCRIPT_NAME", ""),
        "data": data,
    }
    encoded = json.dumps(scope, cls=DjangoJSONEncoder, sort_keys=True, separators=(",", ":"))
    return "h1." + salted_hmac("core.api.human-profile-v1", encoded, algorithm="sha256").hexdigest()


def catalog_projection(kind, row):
    data = {
        key: native_id(row.pk) if key == "id" else getattr(row, key) for key in CATALOG_FIELDS[kind]
    }
    if kind == "merits-flaws":
        ratings = row._profile_ratings
        allowed = row._profile_allowed_types
        if len(ratings) > RELATION_LIMIT or len(allowed) > RELATION_LIMIT:
            raise ProfileError("profile_limit", "catalog_definition")
        data["ratings"] = sorted(item.value for item in ratings)
        data["allowed_types"] = [
            {
                "id": native_id(item.pk),
                "name": item.name,
                "type": item.type,
                "gameline": item.gameline,
            }
            for item in allowed
        ]
    return data
