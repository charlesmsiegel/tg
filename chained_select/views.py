"""
Views for Chained Select AJAX endpoints.

Includes an auto-discovery view that dynamically imports form classes,
so no manual URL configuration is needed.
"""

import importlib

from django.http import JsonResponse
from django.views import View


def auto_chained_ajax_view(request):
    """
    Auto-discovery AJAX view that dynamically imports the form class.

    This is automatically registered at /__chained_select__/

    Query parameters:
        - form: Full path to form class (e.g., 'myapp.forms.MageFactionForm')
        - field: Name of the field to get choices for
        - parent_value: Value of the parent field
    """
    form_path = request.GET.get("form")
    field_name = request.GET.get("field")
    parent_value = request.GET.get("parent_value")

    if not form_path or not field_name:
        return JsonResponse({"error": "Missing required parameters: form, field"}, status=400)

    try:
        # Parse form path: 'myapp.forms.MageFactionForm'
        module_path, class_name = form_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        form_class = getattr(module, class_name)

        # Instantiate form to access field configuration
        form = form_class()
        field = form.fields.get(field_name)

        if not field:
            return JsonResponse({"error": f'Field "{field_name}" not found on form'}, status=400)

        # Get the choices callback
        choices_callback = getattr(field, "choices_callback", None)

        if not choices_callback:
            return JsonResponse(
                {"error": f'Field "{field_name}" has no choices_callback'}, status=400
            )

        # Call the callback to get choices
        choices = choices_callback(parent_value)

        # Normalize to list of {value, label} dicts
        choices_list = []
        for item in choices:
            if isinstance(item, (list, tuple)) and len(item) >= 2:
                choices_list.append({"value": str(item[0]), "label": str(item[1])})
            elif hasattr(item, "pk"):
                choices_list.append({"value": str(item.pk), "label": str(item)})

        return JsonResponse({"choices": choices_list})

    except (ValueError, ImportError, AttributeError) as e:
        return JsonResponse({"error": f"Could not load form: {e}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
            choices_list = []
            for item in choices:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    choices_list.append({"value": str(item[0]), "label": str(item[1])})
                elif hasattr(item, "pk"):
                    # Model instance
                    choices_list.append({"value": str(item.pk), "label": str(item)})

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
