import json

from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe


class AutocompleteTextInput(TextInput):
    def __init__(self, suggestions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions = suggestions or []

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["suggestions"] = self.suggestions
        return context

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        suggestions_js = json.dumps(self.suggestions)
        # Use json.dumps for the name to properly escape for JavaScript context
        name_js = json.dumps(name)
        autocomplete_js = """
            <script>
            $(function() {{
                var suggestions = {suggestions_js};
                var fieldName = {name_js};
                $('input[name="' + fieldName + '"]').autocomplete({{
                    source: suggestions,
                    minLength: 2
                }});
            }});
            </script>
        """.format(
            name_js=name_js, suggestions_js=suggestions_js
        )
        return mark_safe(html + autocomplete_js)
