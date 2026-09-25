"""Views for registered chained-select AJAX endpoints."""

from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_GET

from .utils import normalize_choices


def _mage_creation_form(request):
    # This form needs a user; the registry supplies it from the authenticated request.
    from characters.forms.mage.mage import MageCreationForm  # deferred: circular import

    return MageCreationForm(user=request.user)


REGISTERED_FORMS = {
    "characters.forms.mage.mage.MageCreationForm": (
        _mage_creation_form,
        frozenset({"faction", "subfaction"}),
    ),
}


def _allowed_mage_parent(form, field_name, parent_id):
    from characters.models.mage.faction import MageFaction  # deferred: circular import

    affiliation_ids = form.fields["affiliation"].queryset.values("pk")
    if field_name == "faction":
        return MageFaction.objects.filter(
            pk=parent_id, parent=None, pk__in=affiliation_ids
        ).exists()
    return MageFaction.objects.filter(pk=parent_id, parent_id__in=affiliation_ids).exists()


@require_GET
def auto_chained_ajax_view(request):
    """Return choices only for explicitly registered form fields and parents."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    registration = REGISTERED_FORMS.get(request.GET.get("form"))
    field_name = request.GET.get("field")
    parent_value = request.GET.get("parent_value", "")
    if registration is None or field_name not in registration[1]:
        return JsonResponse({"error": "Unknown form or field"}, status=400)
    if not parent_value.isascii() or not parent_value.isdecimal() or len(parent_value) > 20:
        return JsonResponse({"error": "Invalid parent"}, status=400)
    parent_id = int(parent_value)
    if parent_id < 1:
        return JsonResponse({"error": "Invalid parent"}, status=400)

    form = registration[0](request)
    if not _allowed_mage_parent(form, field_name, parent_id):
        return JsonResponse({"error": "Invalid parent"}, status=400)
    callback = form.fields[field_name].choices_callback
    return JsonResponse({"choices": normalize_choices(callback(parent_id))})


class ChainedSelectAjaxView(View):
    """
    Generic AJAX view for chained select choices.

    Override get_choices() to provide choices based on the field and parent value.

    Example:
        class MyAjaxView(ChainedSelectAjaxView):
            def get_choices(self, field_name, parent_value, request):
                if field_name == 'faction':
                    return Faction.objects.filter(
                        affiliation_id=parent_value
                    ).values_list('id', 'name')
                return []
    """

    def get(self, request):
        field_name = request.GET.get("field")
        parent_value = request.GET.get("parent_value")

        if not field_name:
            return JsonResponse({"error": "field parameter required"}, status=400)

        try:
            choices = self.get_choices(field_name, parent_value, request)

            # Normalize to list of {value, label} dicts
            choices_list = normalize_choices(choices)

            return JsonResponse({"choices": choices_list})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get_choices(self, field_name, parent_value, request):
        """Override this to return choices for the given field and parent."""
        return []


def make_ajax_view(choices_config):
    """
    Factory function to create an AJAX view from a config dict.

    Args:
        choices_config: Dict mapping field names to:
            - A callable(parent_value) that returns choices
            - A dict with 'model', 'parent_field' for simple FK lookups

    Example:
        ajax_view = make_ajax_view({
            'faction': lambda parent: Faction.objects.filter(affiliation=parent),
            'subfaction': {
                'model': Subfaction,
                'parent_field': 'faction_id',
            },
        })

        # urls.py
        path('ajax/chained/', ajax_view, name='chained_ajax'),
    """

    class ConfiguredAjaxView(ChainedSelectAjaxView):
        def get_choices(self, field_name, parent_value, request):
            if field_name not in choices_config:
                return []

            config = choices_config[field_name]

            if callable(config):
                result = config(parent_value)
            elif isinstance(config, dict):
                model = config["model"]
                parent_field = config.get("parent_field", "parent_id")
                qs = model.objects.filter(**{parent_field: parent_value})
                return [(obj.pk, str(obj)) for obj in qs]
            else:
                return []

            # Handle querysets
            if hasattr(result, "values_list"):
                return list(result.values_list("pk", flat=False))
            if hasattr(result, "__iter__"):
                return list(result)
            return []

    return ConfiguredAjaxView.as_view()
