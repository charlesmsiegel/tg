"""Validated writes for the first API increment; no mechanics or ownership writes."""

import json

from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework.exceptions import ValidationError as SerializerValidationError

from characters.models.core import Human
from core.api.serializers import CharacterDescriptionSerializer, ChronicleCreateSerializer
from core.permissions import PermissionManager
from game.models import Chronicle


def payload(body):
    try:
        return json.loads(body)
    except (ValueError, UnicodeDecodeError, RecursionError) as exc:
        raise ValidationError("Malformed JSON.") from exc


def validated(serializer):
    try:
        serializer.is_valid(raise_exception=True)
    except SerializerValidationError as exc:
        raise ValidationError(str(exc.detail)) from exc
    return serializer.validated_data


def update_description(character, body):
    data = validated(CharacterDescriptionSerializer(data=payload(body)))
    if not isinstance(character, Human) and set(data) & {"history", "goals"}:
        raise ValidationError("History and goals require a Human character.")
    for field, value in data.items():
        setattr(character, field, value)
    character.save()
    return character


def create_chronicle(user, body, request):
    # Same scope rule as StorytellerRequiredMixin for ChronicleCreateView: with no
    # target chronicle, only staff/admin can create one, not arbitrary assigned STs.
    if not PermissionManager.can_manage_chronicle(user, None, request=request):
        raise PermissionDenied("Staff permission required to create a chronicle.")
    data = validated(ChronicleCreateSerializer(data=payload(body)))
    return Chronicle.objects.create(head_st=user, **data)
