"""
Limited edit forms for item owners.

These forms restrict owners to editing only descriptive fields (description, public_info)
and prevent them from directly modifying mechanical fields (stats, properties, etc.).

Only Chronicle Head STs and Admins can directly edit mechanical fields.
"""

from django import forms

from items.models.core.item import ItemModel


class LimitedItemEditForm(forms.ModelForm):
    """
    Limited edit form for ItemModel (base).

    Owners can only edit:
    - description (item description)
    - public_info (publicly visible information)
    - image (item image)

    Owners CANNOT edit:
    - name, status, chronicle
    - Any mechanical fields (owned_by, located_at, stats, etc.)
    """

    class Meta:
        model = ItemModel
        fields = [
            'description',
            'public_info',
            'image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Item description, appearance, history...'
            }),
            'public_info': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Information visible to other players...'
            }),
        }
        help_texts = {
            'description': 'Detailed description of the item',
            'public_info': 'Information other players can see about this item',
            'image': 'Item image (will require ST approval)',
        }
