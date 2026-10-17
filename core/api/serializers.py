"""Explicit native field contracts. Unknown write fields are errors, never ignored."""

from rest_framework import serializers

from game.models import Chronicle


class StrictFieldsMixin:
    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError({"non_field_errors": ["Expected a JSON object."]})
        unknown = set(data) - set(self.fields)
        if unknown:
            raise serializers.ValidationError(
                {key: "Unsupported field." for key in sorted(unknown)}
            )
        return super().to_internal_value(data)


class TextField(serializers.CharField):
    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError("Expected text.")
        return super().to_internal_value(data)


class CharacterDescriptionSerializer(StrictFieldsMixin, serializers.Serializer):
    notes = TextField(required=False, allow_blank=True, trim_whitespace=False)
    description = TextField(required=False, allow_blank=True, trim_whitespace=False)
    public_info = TextField(required=False, allow_blank=True, trim_whitespace=False)
    history = TextField(required=False, allow_blank=True, trim_whitespace=False)
    goals = TextField(required=False, allow_blank=True, trim_whitespace=False)


class ChronicleCreateSerializer(StrictFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Chronicle
        fields = ["name", "theme", "mood", "year", "headings"]
