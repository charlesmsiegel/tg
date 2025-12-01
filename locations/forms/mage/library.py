from django import forms
from locations.models.mage.library import Library


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ("name", "description", "parent", "rank", "faction")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        self.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        self.fields["parent"].empty_label = "Choose a Parent Location"
        self.fields["faction"].empty_label = "Choose a Faction"

    def save(self, commit=True):
        library = super().save(commit=True)
        for _ in range(library.rank):
            library.random_book()
        return library
