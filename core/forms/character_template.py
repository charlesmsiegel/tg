from django import forms
from django.conf import settings

from core.models import CharacterTemplate


class CharacterTemplateForm(forms.ModelForm):
    """Form for creating/editing character templates (ST only)"""

    class Meta:
        model = CharacterTemplate
        fields = [
            "name",
            "gameline",
            "character_type",
            "concept",
            "faction",
            "description",
            "basic_info",
            "attributes",
            "abilities",
            "backgrounds",
            "powers",
            "merits_flaws",
            "specialties",
            "languages",
            "equipment",
            "suggested_freebie_spending",
            "is_public",
            "chronicle",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "gameline": forms.Select(attrs={"class": "form-control"}),
            "character_type": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., mage, vampire, werewolf",
                }
            ),
            "concept": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., Hacker, Detective"}
            ),
            "faction": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Brujah, Glass Walkers, Virtual Adepts",
                }
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Template description and background"}
            ),
            "basic_info": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 6,
                    "placeholder": '{"nature": "FK:Archetype:Survivor", "demeanor": "FK:Archetype:Loner"}',
                }
            ),
            "attributes": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 4,
                    "placeholder": '{"strength": 2, "dexterity": 3, "stamina": 2, ...}',
                }
            ),
            "abilities": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 4,
                    "placeholder": '{"alertness": 2, "investigation": 3, ...}',
                }
            ),
            "backgrounds": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 4,
                    "placeholder": '[{"name": "Contacts", "rating": 3}, {"name": "Resources", "rating": 2}]',
                }
            ),
            "powers": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 4,
                    "placeholder": '{"auspex": 2, "celerity": 1} or {"correspondence": 2, "forces": 1}',
                }
            ),
            "merits_flaws": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 4,
                    "placeholder": '[{"name": "Eidetic Memory", "rating": 2}]',
                }
            ),
            "specialties": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 3,
                    "placeholder": '["Firearms (Pistols)", "Computer (Hacking)"]',
                }
            ),
            "languages": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 2,
                    "placeholder": '["English", "Latin", "Spanish"]',
                }
            ),
            "equipment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Starting equipment description",
                }
            ),
            "suggested_freebie_spending": forms.Textarea(
                attrs={
                    "class": "form-control font-monospace",
                    "rows": 3,
                    "placeholder": '{"disciplines": 5, "willpower": 3, "backgrounds": 2}',
                }
            ),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "chronicle": forms.Select(attrs={"class": "form-control"}),
        }
        help_texts = {
            "name": "Display name for the template",
            "gameline": "Which game line this template is for",
            "character_type": "Specific character type (lowercase, e.g., 'mage', 'vampire', 'werewolf')",
            "concept": "Brief character concept (e.g., 'Hacker', 'Street Preacher')",
            "faction": "Optional faction/clan/tribe/tradition (e.g., 'Brujah', 'Glass Walkers', 'Virtual Adepts')",
            "description": "Full description of the character concept and playstyle",
            "basic_info": "JSON: Nature, demeanor, etc. Use 'FK:Archetype:Name' for foreign keys",
            "attributes": "JSON: Attribute ratings (strength, dexterity, etc.)",
            "abilities": "JSON: Ability ratings (alertness, investigation, etc.)",
            "backgrounds": "JSON: List of background objects with name and rating",
            "powers": "JSON: Supernatural powers (disciplines, spheres, gifts, etc.)",
            "merits_flaws": "JSON: List of merit/flaw objects with name and rating",
            "specialties": "JSON: List of strings in 'Ability (Specialty)' format",
            "languages": "JSON: List of language names",
            "equipment": "Text description of starting equipment",
            "suggested_freebie_spending": "JSON: Suggested freebie point allocation",
            "is_public": "Make this template available to all users (uncheck for chronicle-only)",
            "chronicle": "Optional: Restrict template to a specific chronicle",
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Filter chronicle choices to only those where user is ST
        if user and user.is_authenticated:
            from game.models import Chronicle

            user_st_chronicles = Chronicle.objects.filter(storytellers=user)
            self.fields["chronicle"].queryset = user_st_chronicles
            self.fields["chronicle"].required = False

    def clean(self):
        cleaned_data = super().clean()

        # Ensure owner is set to current user
        if self.user:
            self.instance.owner = self.user

        # Mark as user-created (not official)
        self.instance.is_official = False

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Ensure owner is set
        if self.user:
            instance.owner = self.user

        # Mark as user-created
        instance.is_official = False

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class CharacterTemplateImportForm(forms.Form):
    """Form for importing a template from JSON"""

    json_file = forms.FileField(
        label="Template JSON File",
        help_text="Upload a .json file exported from another template",
        widget=forms.FileInput(attrs={"class": "form-control", "accept": ".json"}),
    )

    is_public = forms.BooleanField(
        required=False,
        initial=False,
        label="Make Public",
        help_text="Make this imported template available to all users",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    chronicle = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label="Chronicle",
        help_text="Optional: Restrict template to a specific chronicle",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Filter chronicle choices to only those where user is ST
        if user and user.is_authenticated:
            from game.models import Chronicle

            user_st_chronicles = Chronicle.objects.filter(storytellers=user)
            self.fields["chronicle"].queryset = user_st_chronicles

    def clean_json_file(self):
        json_file = self.cleaned_data.get("json_file")

        if not json_file:
            raise forms.ValidationError("No file uploaded")

        # Check file size (max 5MB)
        if json_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size exceeds 5MB limit")

        # Check file extension
        if not json_file.name.endswith(".json"):
            raise forms.ValidationError("File must be a .json file")

        return json_file
