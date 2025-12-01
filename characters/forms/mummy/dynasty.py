from characters.models.mummy.dynasty import Dynasty
from django import forms


class DynastyForm(forms.ModelForm):
    class Meta:
        model = Dynasty
        fields = [
            "name",
            "description",
            "era",
            "favored_hekau",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Enter dynasty name"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description"})
        self.fields["era"].widget.attrs.update({"placeholder": "e.g., Old Kingdom, Middle Kingdom"})
        self.fields["favored_hekau"].widget.attrs.update(
            {"placeholder": "e.g., Alchemy, Necromancy"}
        )
