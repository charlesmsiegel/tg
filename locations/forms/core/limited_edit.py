"""
Limited edit forms for location owners.

These forms restrict owners to editing only descriptive fields (description, public_info)
and prevent them from directly modifying mechanical fields (stats, properties, etc.).

Only Chronicle Head STs and Admins can directly edit mechanical fields.
"""

from django import forms

from locations.models.core.location import LocationModel


class LimitedLocationEditForm(forms.ModelForm):
    """
    Limited edit form for LocationModel (base).

    Owners can only edit:
    - description (location description)
    - public_info (publicly visible information)
    - image (location image)

    Owners CANNOT edit:
    - name, status, chronicle
    - Any mechanical fields (gauntlet, shroud, dimension_barrier, etc.)
    """

    class Meta:
        model = LocationModel
        fields = [
            "description",
            "public_info",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Location description, features, atmosphere...",
                }
            ),
            "public_info": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Information visible to other players...",
                }
            ),
        }
        help_texts = {
            "description": "Detailed description of the location",
            "public_info": "Information other players can see about this location",
            "image": "Location image (will require ST approval)",
        }
