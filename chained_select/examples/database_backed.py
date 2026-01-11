"""
Example: Database-Backed Chained Selects

For dynamic data stored in the database, just use a choices_callback.
No URL configuration needed - the AJAX endpoint is auto-registered!
"""

from django import forms
from django.db import models

from chained_select import ChainedChoiceField, ChainedSelectMixin

# =============================================================================
# Models
# =============================================================================


class Affiliation(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Faction(models.Model):
    affiliation = models.ForeignKey(Affiliation, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Subfaction(models.Model):
    faction = models.ForeignKey(Faction, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return self.name


# =============================================================================
# Choice callbacks - query the database
# =============================================================================


def get_factions(affiliation_id):
    """Callback to get factions for an affiliation."""
    if not affiliation_id:
        return []
    return list(Faction.objects.filter(affiliation_id=affiliation_id).values_list("id", "name"))


def get_subfactions(faction_id):
    """Callback to get subfactions for a faction."""
    if not faction_id:
        return []
    return list(Subfaction.objects.filter(faction_id=faction_id).values_list("id", "name"))


# =============================================================================
# Form - That's all you need!
# =============================================================================


class DatabaseBackedForm(ChainedSelectMixin, forms.Form):
    """
    Form with database-backed choices.

    No chained_ajax_url needed - the endpoint is auto-registered!
    """

    affiliation = forms.ModelChoiceField(
        queryset=Affiliation.objects.all(),
        empty_label="Select affiliation...",
    )

    faction = ChainedChoiceField(
        parent_field="affiliation",
        choices_callback=get_factions,
        empty_label="Select faction...",
    )

    subfaction = ChainedChoiceField(
        parent_field="faction",
        choices_callback=get_subfactions,
        empty_label="Select subfaction...",
        required=False,
    )


# =============================================================================
# Usage - No URL configuration!
# =============================================================================

"""
# views.py - Just a normal FormView
from django.views.generic import FormView
from .forms import DatabaseBackedForm

class MyView(FormView):
    template_name = 'myapp/form.html'
    form_class = DatabaseBackedForm
    success_url = '/success/'

# urls.py - NO AJAX endpoint needed!
from django.urls import path
from .views import MyView

urlpatterns = [
    path('form/', MyView.as_view()),
    # That's it! No AJAX URL to add.
]

# template - Just render the form
'''
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
'''
"""


# =============================================================================
# Hybrid: Static root, database children
# =============================================================================


class HybridForm(ChainedSelectMixin, forms.Form):
    """
    You can mix static and database-backed fields.
    Static fields use embedded JSON, dynamic fields use auto-AJAX.
    """

    # Static root - choices embedded as JSON, no server call
    affiliation = ChainedChoiceField(
        choices=[
            ("traditions", "Traditions"),
            ("technocracy", "Technocracy"),
        ],
        empty_label="Select affiliation...",
    )

    # Database-backed children - uses auto-registered AJAX endpoint
    faction = ChainedChoiceField(
        parent_field="affiliation",
        choices_callback=get_factions,
        empty_label="Select faction...",
    )

    subfaction = ChainedChoiceField(
        parent_field="faction",
        choices_callback=get_subfactions,
        empty_label="Select subfaction...",
        required=False,
    )


# =============================================================================
# Custom AJAX URL (Optional - only if you need it)
# =============================================================================

"""
If you need a custom AJAX endpoint (e.g., for complex permissions or caching),
you can still specify one:

class CustomForm(ChainedSelectMixin, forms.Form):
    chained_ajax_url = '/my/custom/endpoint/'
    # ...

Then create the view with make_ajax_view:

from chained_select import make_ajax_view

my_ajax_view = make_ajax_view({
    'faction': get_factions,
    'subfaction': get_subfactions,
})

# urls.py
path('/my/custom/endpoint/', my_ajax_view),

But for most cases, you don't need this - the auto-registered endpoint works fine.
"""
