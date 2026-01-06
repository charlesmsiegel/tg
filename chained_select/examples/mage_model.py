"""
Example: Mage the Ascension - Self-Referential Faction Model

Uses a single MageFaction model with a parent field to represent
the entire hierarchy: Affiliation -> Faction -> Subfaction

NO URL CONFIGURATION NEEDED - the AJAX endpoint is auto-registered!
"""

from chained_select import ChainedChoiceField, ChainedSelectMixin
from django import forms
from django.db import models

# =============================================================================
# Model - One table for the entire hierarchy
# =============================================================================


class MageFaction(models.Model):
    """
    Self-referential model for the faction hierarchy.

    Level 0 (parent=None): Affiliations (Traditions, Technocracy)
    Level 1: Factions/Traditions/Conventions (Order of Hermes, Iteration X)
    Level 2: Subfactions/Methodologies (House Bonisagus, BioMechanics)

    Can extend to arbitrary depth if needed.
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = ["parent", "slug"]

    def __str__(self):
        return self.name

    @property
    def level(self):
        """Calculate depth in the hierarchy (0 = root)."""
        level = 0
        node = self
        while node.parent:
            level += 1
            node = node.parent
        return level

    @classmethod
    def get_roots(cls):
        """Get top-level factions (affiliations)."""
        return cls.objects.filter(parent__isnull=True)

    @classmethod
    def get_children_of(cls, parent_id):
        """Get direct children of a faction."""
        if not parent_id:
            return cls.objects.none()
        return cls.objects.filter(parent_id=parent_id)


# =============================================================================
# Choice helper function - works for any level!
# =============================================================================


def get_children(parent_id):
    """Get children of any faction - works for any level."""
    if not parent_id:
        return []
    return list(MageFaction.objects.filter(parent_id=parent_id).values_list("id", "name"))


# =============================================================================
# Form - That's all you need!
# =============================================================================


class MageFactionForm(ChainedSelectMixin, forms.Form):
    """
    Three-level faction selector using the self-referential model.

    No chained_ajax_url needed - it's auto-registered at /__chained_select__/
    """

    affiliation = forms.ModelChoiceField(
        queryset=MageFaction.objects.filter(parent__isnull=True),
        label="Affiliation",
        empty_label="Select affiliation...",
        required=True,
    )

    faction = ChainedChoiceField(
        parent_field="affiliation",
        choices_callback=get_children,
        label="Tradition / Convention",
        empty_label="Select tradition/convention...",
        required=True,
    )

    subfaction = ChainedChoiceField(
        parent_field="faction",
        choices_callback=get_children,  # Same function works for any level!
        label="Subfaction / Methodology",
        empty_label="Select subfaction...",
        required=False,
    )

    def clean_faction(self):
        """Convert faction ID to model instance."""
        faction_id = self.cleaned_data.get("faction")
        if faction_id:
            try:
                return MageFaction.objects.get(pk=faction_id)
            except MageFaction.DoesNotExist:
                raise forms.ValidationError("Invalid faction selected.")
        return None

    def clean_subfaction(self):
        """Convert subfaction ID to model instance."""
        subfaction_id = self.cleaned_data.get("subfaction")
        if subfaction_id:
            try:
                return MageFaction.objects.get(pk=subfaction_id)
            except MageFaction.DoesNotExist:
                raise forms.ValidationError("Invalid subfaction selected.")
        return None


# =============================================================================
# That's it! No AJAX view or URL configuration needed!
# =============================================================================

# The AppConfig automatically registers /__chained_select__/ which:
# 1. Receives the form path (e.g., 'myapp.forms.MageFactionForm')
# 2. Dynamically imports the form class
# 3. Instantiates it to get the field's choices_callback
# 4. Calls the callback with the parent value
# 5. Returns the choices as JSON


# =============================================================================
# Example View - Just a normal FormView
# =============================================================================

"""
# views.py
from django.views.generic import FormView
from .forms import MageFactionForm

class CharacterCreateView(FormView):
    template_name = 'mage/character_create.html'
    form_class = MageFactionForm
    success_url = '/characters/'
    
    def form_valid(self, form):
        data = form.cleaned_data
        
        # All three are now MageFaction instances (or None for subfaction)
        affiliation = data['affiliation']  # MageFaction instance
        faction = data['faction']          # MageFaction instance  
        subfaction = data['subfaction']    # MageFaction instance or None
        
        # Create your character
        # Character.objects.create(
        #     affiliation=affiliation,
        #     faction=faction,
        #     subfaction=subfaction,
        # )
        
        return super().form_valid(form)
"""


# =============================================================================
# URL Configuration - NOTHING NEEDED!
# =============================================================================

"""
# urls.py - No chained select URLs needed!
from django.urls import path
from .views import CharacterCreateView

urlpatterns = [
    path('character/create/', CharacterCreateView.as_view(), name='character_create'),
    # That's it! No AJAX endpoint to add.
]
"""


# =============================================================================
# Template - Just render the form, nothing else needed!
# =============================================================================

"""
<!-- templates/mage/character_create.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Create Character</title>
    <!-- No {{ form.media }} needed! JavaScript auto-injects. -->
</head>
<body>
    <h1>Create Mage Character</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Create Character</button>
    </form>
</body>
</html>
"""


# =============================================================================
# Data Migration - Populate the hierarchy
# =============================================================================

"""
# migrations/0002_populate_mage_factions.py

from django.db import migrations


def populate_factions(apps, schema_editor):
    MageFaction = apps.get_model('yourapp', 'MageFaction')
    
    # Create affiliations (level 0)
    traditions = MageFaction.objects.create(
        name='Council of Nine Mystic Traditions',
        slug='traditions',
        parent=None
    )
    technocracy = MageFaction.objects.create(
        name='Technocratic Union', 
        slug='technocracy',
        parent=None
    )
    
    # Create traditions (level 1)
    tradition_data = [
        ('akashic', 'Akashic Brotherhood'),
        ('celestial-chorus', 'Celestial Chorus'),
        ('cult-of-ecstasy', 'Cult of Ecstasy'),
        ('dreamspeakers', 'Dreamspeakers'),
        ('euthanatos', 'Euthanatos'),
        ('order-of-hermes', 'Order of Hermes'),
        ('sons-of-ether', 'Sons of Ether'),
        ('verbena', 'Verbena'),
        ('virtual-adepts', 'Virtual Adepts'),
    ]
    
    tradition_objs = {}
    for slug, name in tradition_data:
        tradition_objs[slug] = MageFaction.objects.create(
            name=name, slug=slug, parent=traditions
        )
    
    # Create conventions (level 1)
    convention_data = [
        ('iteration-x', 'Iteration X'),
        ('new-world-order', 'New World Order'),
        ('progenitors', 'Progenitors'),
        ('syndicate', 'Syndicate'),
        ('void-engineers', 'Void Engineers'),
    ]
    
    convention_objs = {}
    for slug, name in convention_data:
        convention_objs[slug] = MageFaction.objects.create(
            name=name, slug=slug, parent=technocracy
        )
    
    # Create subfactions (level 2)
    # Order of Hermes Houses
    hermes_houses = [
        ('bonisagus', 'House Bonisagus'),
        ('criamon', 'House Criamon'),
        ('ex-miscellanea', 'House Ex Miscellanea'),
        ('flambeau', 'House Flambeau'),
        ('fortunae', 'House Fortunae'),
        ('hong-lei', 'House Hong Lei'),
        ('janissary', 'House Janissary'),
        ('merinita', 'House Merinita'),
        ('quaesitor', 'House Quaesitor'),
        ('shaea', 'House Shaea'),
        ('skopos', 'House Skopos'),
        ('solificati', 'House Solificati'),
        ('tharsis', 'House Tharsis'),
        ('tytalus', 'House Tytalus'),
        ('verditius', 'House Verditius'),
        ('xaos', 'House Xaos'),
    ]
    for slug, name in hermes_houses:
        MageFaction.objects.create(
            name=name, slug=slug, parent=tradition_objs['order-of-hermes']
        )
    
    # Iteration X Methodologies
    itx_methodologies = [
        ('biomechanics', 'BioMechanics'),
        ('macrotechnicians', 'Macrotechnicians'),
        ('statisticians', 'Statisticians'),
        ('time-motion', 'Time-Motion Managers'),
    ]
    for slug, name in itx_methodologies:
        MageFaction.objects.create(
            name=name, slug=slug, parent=convention_objs['iteration-x']
        )
    
    # ... continue for other traditions/conventions ...


def depopulate_factions(apps, schema_editor):
    MageFaction = apps.get_model('yourapp', 'MageFaction')
    MageFaction.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('yourapp', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(populate_factions, depopulate_factions),
    ]
"""


# =============================================================================
# Management Command Alternative - For loading from fixture/data file
# =============================================================================

"""
# management/commands/load_mage_factions.py

from django.core.management.base import BaseCommand
from yourapp.models import MageFaction

FACTION_TREE = {
    'Council of Nine Mystic Traditions': {
        'Akashic Brotherhood': [
            'Kannagara', 'Li-Hai', 'Mo-Ai', 'Shaolin', 'Vajrapani', 'Wu Lung'
        ],
        'Celestial Chorus': [
            'Alexandrian Society', 'Anchorite', 'Latitudinarian', 
            'Monist', 'Nashimite', 'Septarian', 'Song of the Ancients'
        ],
        'Cult of Ecstasy': [
            'Aghoris', 'Club Kids', 'Dissonance Society', 
            "Children of Freyja", 'Joybringers', 'Maenad', "K'an Lu / Acharne"
        ],
        'Dreamspeakers': [
            'Balombe', 'Baruti', 'Ghost Wheel Society', 
            'Kopa Loei', 'Red Spear Society', 'Spirit Smiths', 'Solitaries'
        ],
        'Euthanatos': [
            'Aided', 'Albireo', 'Chakravanti', 'Golden Chalice',
            'Lhaksmists', 'Madzimbabwe', 'Natatapas', 'Pomegranate Deme', 'Vrati'
        ],
        'Order of Hermes': [
            'House Bonisagus', 'House Criamon', 'House Ex Miscellanea',
            'House Flambeau', 'House Fortunae', 'House Hong Lei',
            'House Janissary', 'House Merinita', 'House Quaesitor',
            'House Shaea', 'House Skopos', 'House Solificati',
            'House Tharsis', 'House Tytalus', 'House Verditius', 'House Xaos'
        ],
        'Sons of Ether': [
            'Adventurers', 'Cybernauts', 'Ethernauts', 
            'Mad Scientists', 'Progressivists', 'Utopians'
        ],
        'Verbena': [
            'Gardeners of the Tree', 'Lifeweavers', 'Moon-Seekers',
            'Twisters of Fate', 'Techno-Pagans'
        ],
        'Virtual Adepts': [
            'Cypherpunks', 'Chaoticians', 'Cyberpunks', 'Nexplorers', 'Reality Coders'
        ],
    },
    'Technocratic Union': {
        'Iteration X': [
            'BioMechanics', 'Macrotechnicians', 'Statisticians', 'Time-Motion Managers'
        ],
        'New World Order': [
            'Ivory Tower', 'Operatives', 'Q Division', 'Watchers'
        ],
        'Progenitors': [
            'FACADE Engineers', 'Genegineers', 'Pharmacopoeists',
            'Preservationists', 'Shalihotran Society'
        ],
        'Syndicate': [
            'Disbursements', 'Enforcers', 'Financiers',
            'Media Control', 'Special Projects Division'
        ],
        'Void Engineers': [
            'Border Corps Division', 'Deep Exploration Teams',
            'Earth Frontier Division', 'Neutralization Specialist Corps',
            'Pan-Dimensional Corps', 'Research & Execution'
        ],
    },
}


class Command(BaseCommand):
    help = 'Load Mage faction hierarchy'
    
    def make_slug(self, name):
        return name.lower().replace(' ', '-').replace("'", '').replace('/', '-')
    
    def handle(self, *args, **options):
        # Clear existing
        MageFaction.objects.all().delete()
        
        for affiliation_name, factions in FACTION_TREE.items():
            affiliation = MageFaction.objects.create(
                name=affiliation_name,
                slug=self.make_slug(affiliation_name),
                parent=None
            )
            self.stdout.write(f'Created affiliation: {affiliation_name}')
            
            for faction_name, subfactions in factions.items():
                faction = MageFaction.objects.create(
                    name=faction_name,
                    slug=self.make_slug(faction_name),
                    parent=affiliation
                )
                self.stdout.write(f'  Created faction: {faction_name}')
                
                for subfaction_name in subfactions:
                    MageFaction.objects.create(
                        name=subfaction_name,
                        slug=self.make_slug(subfaction_name),
                        parent=faction
                    )
                self.stdout.write(f'    Created {len(subfactions)} subfactions')
        
        total = MageFaction.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Loaded {total} factions'))
"""
