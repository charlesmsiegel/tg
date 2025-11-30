from characters.models.mummy.mummy_title import MummyTitle
from django import forms


class MummyTitleForm(forms.ModelForm):
    class Meta:
        model = MummyTitle
        fields = [
            "name",
            "rank_level",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"placeholder": "Enter title name"})
        self.fields["description"].widget.attrs.update(
            {"placeholder": "Enter description"}
        )
