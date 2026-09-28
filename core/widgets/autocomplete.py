from django.forms.widgets import TextInput
from django.utils.html import format_html, format_html_join


class AutocompleteTextInput(TextInput):
    """A text input that suggests values through a native ``<datalist>``.

    No JavaScript: the browser offers the suggestions as the user types, and they are
    escaped like any other markup. (It used to call jQuery UI's autocomplete from an
    inline script; the Spread pages load neither jQuery nor jQuery UI.)
    """

    def __init__(self, suggestions=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.suggestions = suggestions or []

    @staticmethod
    def list_id(name, attrs):
        return f"{(attrs or {}).get('id') or name}-suggestions"

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["suggestions"] = self.suggestions
        context["widget"]["attrs"]["list"] = self.list_id(name, context["widget"]["attrs"])
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        html = self._render(self.template_name, context, renderer)
        options = format_html_join(
            "", '<option value="{}"></option>', ((suggestion,) for suggestion in self.suggestions)
        )
        return format_html(
            '{}<datalist id="{}">{}</datalist>', html, context["widget"]["attrs"]["list"], options
        )
