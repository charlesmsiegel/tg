# Characters App

The `characters` app manages player and NPC characters across all World of Darkness gamelines. It uses polymorphic inheritance to support gameline-specific character types while sharing common functionality.

## Purpose

The characters app provides:
- Character creation and management for all WoD gamelines
- Polymorphic character models (VtM, WtA, MtA, WtO, CtD, DtF)
- Character sheets with gameline-specific traits
- XP tracking and spending approval workflows
- Character status management (Unfinished → Submitted → Approved)
- Gameline-specific forms, views, and templates

## Supported Gamelines

- **Vampire: The Masquerade (VtM)** - Vampires with Disciplines, blood pools, clans
- **Werewolf: The Apocalypse (WtA)** - Garou with Gifts, Rage, Gnosis
- **Mage: The Ascension (MtA)** - Mages with Spheres, Arete, Traditions/Conventions
- **Wraith: The Oblivion (WtO)** - Wraiths with Arcanoi, Corpus, Passions/Fetters
- **Changeling: The Dreaming (CtD)** - Changelings with Arts, Glamour, seemings
- **Demon: The Fallen (DtF)** - Demons with Lores, Torment, Houses

## Directory Structure

```
characters/
├── __init__.py
├── admin.py                    # Admin configuration
├── apps.py                     # App configuration
├── forms/                      # Character creation/edit forms
│   ├── __init__.py
│   ├── core/                   # Shared form components
│   ├── vampire/                # VtM-specific forms
│   ├── werewolf/               # WtA-specific forms
│   ├── mage/                   # MtA-specific forms
│   ├── wraith/                 # WtO-specific forms
│   ├── changeling/             # CtD-specific forms
│   └── demon/                  # DtF-specific forms
├── models/                     # Character models
│   ├── __init__.py
│   ├── core/                   # Base Character class
│   │   ├── character.py        # Main Character model
│   │   ├── ability_block.py    # Talents, Skills, Knowledges
│   │   ├── attribute_block.py  # Physical, Social, Mental
│   │   └── ...
│   ├── vampire/                # VtM character types
│   │   ├── vtm.py             # VtMHuman base
│   │   ├── vampire.py         # Vampire-specific model
│   │   └── ...
│   ├── werewolf/               # WtA character types
│   ├── mage/                   # MtA character types
│   ├── wraith/                 # WtO character types
│   ├── changeling/             # CtD character types
│   └── demon/                  # DtF character types
├── templates/
│   └── characters/
│       ├── core/               # Base character templates
│       ├── vampire/            # VtM templates
│       ├── werewolf/           # WtA templates
│       ├── mage/               # MtA templates
│       ├── wraith/             # WtO templates
│       ├── changeling/         # CtD templates
│       └── demon/              # DtF templates
├── templatetags/               # Custom template tags
├── tests/                      # Tests by gameline
│   ├── vampire/
│   ├── werewolf/
│   ├── mage/
│   └── ...
├── urls/                       # URL routing by gameline
│   ├── __init__.py
│   ├── vampire/
│   ├── werewolf/
│   └── ...
└── views/                      # Views by gameline
    ├── __init__.py
    ├── core/                   # Shared view logic
    ├── vampire/
    ├── werewolf/
    └── ...
```

## Key Components

### Base Character Model

All characters inherit from `Character` in `models/core/character.py`:

```python
from core.models import Model

class Character(Model):
    # Core fields shared across all gamelines
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chronicle = models.ForeignKey('game.Chronicle', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='Un')

    # XP tracking
    xp = models.IntegerField(default=0)
    spent_xp = models.JSONField(default=dict)

    # Character creation
    freebies = models.IntegerField(default=15)
    concept = models.CharField(max_length=100)

    # Methods
    def add_xp(self, amount):
        """Add XP to character."""

    def spend_xp(self, trait, cost):
        """Spend XP on trait (requires ST approval)."""
```

### Gameline-Specific Models

Each gameline has specific character implementations:

**Vampire (VtM):**
```python
class VtMHuman(Character):
    # Vampire-specific fields
    clan = models.ForeignKey('Clan', on_delete=models.SET_NULL, null=True)
    sire = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    generation = models.IntegerField(default=13)

class Vampire(VtMHuman):
    # Blood and disciplines
    blood_pool = models.IntegerField(default=10)
    blood_max = models.IntegerField(default=10)
    disciplines = models.JSONField(default=dict)
```

**Werewolf (WtA):**
```python
class Werewolf(Character):
    # Garou-specific fields
    breed = models.CharField(max_length=20)
    auspice = models.CharField(max_length=20)
    tribe = models.ForeignKey('Tribe', on_delete=models.SET_NULL, null=True)

    # Werewolf resources
    rage = models.IntegerField(default=0)
    gnosis = models.IntegerField(default=0)
    gifts = models.JSONField(default=dict)
```

**Mage (MtA):**
```python
class Mage(Character):
    # Mage-specific fields
    essence = models.CharField(max_length=20)
    affiliation = models.CharField(max_length=20)  # Tradition/Convention

    # Mage resources
    arete = models.IntegerField(default=0)
    quintessence = models.IntegerField(default=0)
    spheres = models.JSONField(default=dict)
```

### Forms

Forms are organized by gameline in `forms/`:

- **Core forms** - Shared form components and mixins
- **Gameline forms** - Character creation/editing for specific gamelines

Example:
```python
# forms/vampire/vampire.py
class VampireForm(forms.ModelForm):
    class Meta:
        model = Vampire
        fields = ['name', 'clan', 'generation', 'disciplines', ...]
```

### Views

Views follow Django's class-based view pattern:

```python
# views/vampire/vampire.py
class VampireDetailView(DetailView):
    model = Vampire
    template_name = 'characters/vampire/vampire/detail.html'

class VampireCreateView(CreateView):
    model = Vampire
    form_class = VampireForm
    template_name = 'characters/vampire/vampire/create.html'
```

## Character Creation Workflow

1. **Create Character** - User selects gameline and character type
2. **Fill Details** - Enter character concept, attributes, abilities
3. **Spend Points** - Allocate creation points (Attributes, Abilities, Backgrounds)
4. **Spend Freebies** - Use freebie points for final customization
5. **Submit** - Change status from 'Unfinished' to 'Submitted'
6. **ST Review** - Storyteller reviews and approves/rejects
7. **Approved** - Character ready for play

## XP System

### Earning XP
- Awarded by Storyteller after sessions
- Tracked in `character.xp` field

### Spending XP
- Player records XP expenditure in `character.spent_xp` JSONField
- Requires Storyteller approval
- Format: `{"trait_name": cost, "approved": False}`

Example:
```python
character.spend_xp("Celerity 2", 10)
# spent_xp = {"Celerity 2": 10, "approved": False}
```

## Character Status

Characters progress through status stages:

- **Un (Unfinished)** - Character in creation
- **Sub (Submitted)** - Awaiting ST approval
- **App (Approved)** - Ready for play
- **Ret (Retired)** - No longer active
- **Dec (Deceased)** - Character died

## Usage Examples

### Creating a Vampire

```python
from characters.models.vampire import Vampire
from accounts.models import Profile

vampire = Vampire.objects.create(
    owner=user,
    name="Lucian Drake",
    concept="Street Tough",
    clan=clan_brujah,
    generation=13,
    status='Un'
)
```

### Querying Characters

```python
# Get all characters for a user
my_characters = Character.objects.filter(owner=request.user)

# Get all vampires in a chronicle
vampires = Vampire.objects.filter(chronicle=chronicle)

# Get approved mages
mages = Mage.objects.filter(status='App')
```

### Character Sheet URL

```python
# In template
<a href="{{ character.get_absolute_url }}">View Character</a>

# In views
return redirect(character.get_absolute_url())
```

## Testing

Run character tests:
```bash
# All character tests
pytest characters/tests/

# Gameline-specific tests
pytest characters/tests/vampire/
pytest characters/tests/mage/

# Specific test file
pytest -v characters/tests/vampire/test_vampire.py
```

## Permissions

Characters use these permission checks:

- **Owner** - Can edit their own characters
- **Storyteller** - Can edit characters in their chronicles
- **Approved Status** - Only STs can approve characters

Example:
```python
if character.owner == request.user or request.user.profile.is_st():
    # Allow editing
    pass
```

## Related Apps

- **core** - Base models and utilities
- **game** - Chronicles, Scenes, XP awards
- **accounts** - User profiles, ST relationships

## Common Tasks

### Adding a New Character Type

1. Create model in appropriate gameline folder
2. Create form in `forms/{gameline}/`
3. Create views in `views/{gameline}/`
4. Add URL patterns in `urls/{gameline}/`
5. Create templates in `templates/characters/{gameline}/`
6. Add tests in `tests/{gameline}/`

### Adding a New Trait

1. Add field to appropriate model
2. Create migration: `python manage.py makemigrations`
3. Update form to include new field
4. Update template to display trait
5. Add tests for the new trait

## Related Documentation

- See `docs/CODE_STYLE.md` for coding standards
- See `docs/MODELS.md` for model patterns
- See `docs/FORMS.md` for form guidelines
- See `docs/VIEWS.md` for view patterns
- See `docs/TEMPLATES.md` for template structure
- See `/CLAUDE.md` for project-wide conventions
