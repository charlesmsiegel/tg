"""Views for registered chained-select AJAX endpoints."""

from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.views.decorators.http import require_GET

from .utils import normalize_choices

# Dotted form path -> the chained fields the endpoint may serve for it. The form
# is built with the requesting user and decides itself, through
# ``allowed_chained_parent(field_name, parent_id)``, which parents are valid.
REGISTERED_FORMS = {
    "characters.forms.mage.mage.MageCreationForm": frozenset({"faction", "subfaction"}),
}


@require_GET
def auto_chained_ajax_view(request):
    """Return choices only for explicitly registered form fields and parents."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    form_path = request.GET.get("form")
    allowed_fields = REGISTERED_FORMS.get(form_path)
    field_name = request.GET.get("field")
    parent_value = request.GET.get("parent_value", "")
    if allowed_fields is None or field_name not in allowed_fields:
        return JsonResponse({"error": "Unknown form or field"}, status=400)
    if not parent_value.isascii() or not parent_value.isdecimal() or len(parent_value) > 20:
        return JsonResponse({"error": "Invalid parent"}, status=400)
    parent_id = int(parent_value)
    if parent_id < 1:
        return JsonResponse({"error": "Invalid parent"}, status=400)

    form = import_string(form_path)(user=request.user)
    if not form.allowed_chained_parent(field_name, parent_id):
        return JsonResponse({"error": "Invalid parent"}, status=400)
    callback = form.fields[field_name].choices_callback
    return JsonResponse({"choices": normalize_choices(callback(parent_id))})
