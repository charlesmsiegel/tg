from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background
from characters.models.core.merit_flaw_block import MeritFlaw, MeritFlawRating
from characters.models.mage.effect import Effect
from characters.models.mage.resonance import Resonance
from core.widgets import AutocompleteTextInput
from django import forms
from game.models import ObjectType
from items.forms.mage.wonder import WonderForm
from items.models.mage.artifact import Artifact
from items.models.mage.talisman import Talisman
from items.models.mage.wonder import Wonder, WonderResonanceRating


class EnhancementForm(forms.Form):
    enhancement_style = forms.ChoiceField(
        choices=[
            ("Cybernetics", "Cybernetics"),
            ("Biomods", "Biomods"),
            ("Genegineering", "Genegineering"),
        ],
        required=False,
    )
    enhancement_type = forms.ChoiceField(
        choices=[
            ("Attributes", "Attributes"),
            ("Existing Device", "Existing Device"),
            ("New Device", "New Device"),
            ("Health", "Health"),
        ],
        required=False,
    )

    new_device_new_power_option = forms.ChoiceField(
        choices=[
            ("New Effect", "New Effect"),
            ("Existing Effect", "Existing Effect"),
        ],
        required=False,
    )

    new_device_resonance = forms.CharField(
        required=False, widget=AutocompleteTextInput(suggestions=[])
    )

    new_device_effect = forms.ModelChoiceField(queryset=Effect.objects.none(), required=False)

    new_device_new_effect_name = forms.CharField(max_length=100, required=False)
    new_device_new_effect_description = forms.CharField(widget=forms.Textarea(), required=False)
    new_device_new_effect_correspondence = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_time = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_spirit = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_matter = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_life = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_forces = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_entropy = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_mind = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )
    new_device_new_effect_prime = forms.IntegerField(
        min_value=0, max_value=5, initial=0, required=False
    )

    device = forms.ModelChoiceField(queryset=Wonder.objects.none(), required=False)
    flaw = forms.ModelChoiceField(queryset=MeritFlaw.objects.none(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        enhancement_type = cleaned_data.get("enhancement_type")
        enhancement_style = cleaned_data.get("enhancement_style")

        # Validate enhancement_style is selected
        if not enhancement_style:
            raise forms.ValidationError("Enhancement style must be selected.")

        # Validate enhancement_type is selected
        if not enhancement_type:
            raise forms.ValidationError("Enhancement type must be selected.")

        # Type-specific validation
        if enhancement_type == "Attributes":
            # Validate that the correct number of attributes are selected
            selected_attributes = []
            for i in range(self.rank):
                att = cleaned_data.get(f"attribute_{i}")
                if att:
                    selected_attributes.append(att)

            if len(selected_attributes) != self.rank:
                raise forms.ValidationError(
                    f"You must select exactly {self.rank} attribute(s) for this enhancement."
                )

        elif enhancement_type == "Existing Device":
            # Validate that a device is selected
            if not cleaned_data.get("device"):
                raise forms.ValidationError("You must select an existing device.")

        elif enhancement_type == "New Device":
            # Validate new device fields
            new_power_option = cleaned_data.get("new_device_new_power_option")
            wonder_type = cleaned_data.get("new_device_wonder_type")
            resonance = cleaned_data.get("new_device_resonance")

            if not new_power_option:
                raise forms.ValidationError("You must select a power option for the new device.")

            if not wonder_type:
                raise forms.ValidationError("You must select a wonder type for the new device.")

            if not resonance:
                raise forms.ValidationError("You must specify a resonance for the new device.")

            # Validate effect-specific fields
            if new_power_option == "New Effect":
                # Check that new effect fields are filled
                if not cleaned_data.get("new_device_new_effect_name"):
                    raise forms.ValidationError("You must provide a name for the new effect.")

                if not cleaned_data.get("new_device_new_effect_description"):
                    raise forms.ValidationError(
                        "You must provide a description for the new effect."
                    )

                # Validate effect cost
                effect_cost = sum(
                    [
                        cleaned_data.get("new_device_new_effect_correspondence", 0),
                        cleaned_data.get("new_device_new_effect_time", 0),
                        cleaned_data.get("new_device_new_effect_spirit", 0),
                        cleaned_data.get("new_device_new_effect_matter", 0),
                        cleaned_data.get("new_device_new_effect_life", 0),
                        cleaned_data.get("new_device_new_effect_forces", 0),
                        cleaned_data.get("new_device_new_effect_entropy", 0),
                        cleaned_data.get("new_device_new_effect_mind", 0),
                        cleaned_data.get("new_device_new_effect_prime", 0),
                    ]
                )

                if effect_cost > 2 * self.rank:
                    raise forms.ValidationError(
                        f"Effect cost ({effect_cost}) cannot exceed {2 * self.rank} for rank {self.rank} enhancement."
                    )

            elif new_power_option == "Existing Effect":
                # Check that an effect is selected
                if not cleaned_data.get("new_device_effect"):
                    raise forms.ValidationError("You must select an existing effect.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.rank = kwargs.pop("rank", 0)
        suggestions = kwargs.pop("suggestions", None)
        super().__init__(*args, **kwargs)
        if suggestions is None:
            suggestions = [x.name.title() for x in Resonance.objects.order_by("name")]
        self.fields["new_device_resonance"].widget.suggestions = suggestions

        embedded_form = WonderForm()
        for field_name, field in embedded_form.fields.items():
            self.fields["new_device_" + field_name] = field
            self.fields["new_device_" + field_name].label = f"New Device {field.label}"
            self.fields["new_device_" + field_name].required = False
        self.fields["new_device_wonder_type"].choices = [
            ("artifact", "Artifact"),
            ("talisman", "Talisman"),
        ]
        self.fields["new_device_effect"].queryset = Effect.objects.filter(
            rote_cost__lte=2 * self.rank
        )

        for i in range(self.rank):
            self.fields[f"attribute_{i}"] = forms.ModelChoiceField(
                queryset=Attribute.objects.filter(
                    property_name__in=[
                        "strength",
                        "dexterity",
                        "stamina",
                        "appearance",
                        "perception",
                        "intelligence",
                    ]
                ),
                required=False,
            )
        self.fields["flaw"].queryset = MeritFlaw.objects.filter(
            ratings__value__in=[-self.rank],
            allowed_types__in=[
                ObjectType.objects.get_or_create(
                    name="mage", defaults={"type": "char", "gameline": "mta"}
                )[0]
            ],
        )
        self.fields["device"].queryset = Wonder.objects.filter(rank=self.rank).exclude(
            polymorphic_ctype__model="charm"
        )

    def save(self, *args, **kwargs):
        char = kwargs.pop("char", None)
        if char is None:
            raise ValueError("Form requires char keyword")

        note = []

        if self.cleaned_data["enhancement_type"] == "Attributes":
            for i in range(self.rank):
                att = self.cleaned_data[f"attribute_{i}"]
                note.append(att.name)
                char.add_attribute(att.property_name, maximum=10)
            url = ""
        elif self.cleaned_data["enhancement_type"] == "Existing Device":
            char.enhancement_devices.add(self.cleaned_data["device"])
            note.append(self.cleaned_data["device"].name)
            url = self.cleaned_data["device"].get_absolute_url()
        elif self.cleaned_data["enhancement_type"] == "New Device":
            wonder_dict = {
                "artifact": Artifact,
                "talisman": Talisman,
            }
            wonder = wonder_dict[self.cleaned_data["new_device_wonder_type"]]

            if self.cleaned_data["new_device_new_power_option"] == "New Effect":
                effect = Effect(
                    name=self.cleaned_data["new_device_new_effect_name"],
                    description=self.cleaned_data["new_device_new_effect_description"],
                    correspondence=self.cleaned_data["new_device_new_effect_correspondence"],
                    time=self.cleaned_data["new_device_new_effect_time"],
                    spirit=self.cleaned_data["new_device_new_effect_spirit"],
                    matter=self.cleaned_data["new_device_new_effect_matter"],
                    life=self.cleaned_data["new_device_new_effect_life"],
                    forces=self.cleaned_data["new_device_new_effect_forces"],
                    entropy=self.cleaned_data["new_device_new_effect_entropy"],
                    mind=self.cleaned_data["new_device_new_effect_mind"],
                    prime=self.cleaned_data["new_device_new_effect_prime"],
                )
                effect.save()
            elif self.cleaned_data["new_device_new_power_option"] == "Existing Effect":
                effect = self.cleaned_data["new_device_effect"]

            wonder_kwargs = {
                "name": "",
                "description": "",
                "rank": self.rank,
                "background_cost": 2 * self.rank,
                "quintessence_max": 5 * self.rank,
            }
            if self.cleaned_data["new_device_wonder_type"] == "artifact":
                wonder_kwargs.update({"power": effect})
            elif self.cleaned_data["new_device_wonder_type"] == "talisman":
                wonder_kwargs.update({"arete": self.rank})

            w = wonder.objects.create(**wonder_kwargs)
            if self.cleaned_data["new_device_wonder_type"] == "talisman":
                w.powers.add(effect)

            WonderResonanceRating.objects.create(
                wonder=w,
                resonance=Resonance.objects.get_or_create(
                    name=self.cleaned_data["new_device_resonance"], rating=self.rank
                )[0],
            )

            note.append(w.name)
            url = w.get_absolute_url()
        elif self.cleaned_data["enhancement_type"] == "Health":
            char.max_health_levels += self.rank
            for _ in range(self.rank):
                note.append("Health")
            url = ""

        if self.cleaned_data["flaw"] is not None:
            MeritFlawRating.objects.create(
                character=char, mf=self.cleaned_data["flaw"], rating=-self.rank
            )
            note.append(self.cleaned_data["flaw"].name)
        else:
            char.paradox += self.rank
            note.append(f"{self.rank} Permanent Paradox")

        note = ", ".join(note)
        # url

        enhancement_bg, _ = Background.objects.get_or_create(
            property_name="enhancement", defaults={"name": "Enhancement"}
        )
        bgr = char.backgrounds.filter(
            bg=enhancement_bg,
            rating=self.rank,
            complete=False,
        ).first()

        bgr.note = note
        bgr.url = url
        bgr.complete = True
        bgr.save()
