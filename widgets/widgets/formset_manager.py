"""Static media for the formset manager browser manager."""

from django import forms


def render_formset_manager_script():
    """Return external script markup without any request-global state."""
    return forms.Media(js=("widgets/formset_manager.js",)).render_js()[0]
