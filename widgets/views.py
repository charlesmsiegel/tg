"""Views for registered chained-select AJAX endpoints."""

from django.http import JsonResponse
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
