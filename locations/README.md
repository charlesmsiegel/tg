# Locations App

The `locations` app manages places, territories, and special locations across all World of Darkness gamelines. It uses polymorphic inheritance similar to characters and items apps.

## Purpose

The locations app provides:
- Location creation and management for all WoD gamelines
- Polymorphic location models (havens, caerns, chantries, haunts, freeholds, etc.)
- Gameline-specific special locations
- Location ownership and chronicle association
- Location status management (Unfinished → Submitted → Approved)
- Gameline-specific forms, views, and templates

## Supported Location Types

- **Vampire (VtM)** - Havens, Elysiums, domains, feeding grounds
- **Werewolf (WtA)** - Caerns, septs, hunting grounds, bawn
- **Mage (MtA)** - Chantries, Nodes, Realms, sanctums
- **Wraith (WtO)** - Haunts, Citadels, Necropoli
- **Changeling (CtD)** - Freeholds, trods, glens
- **Demon (DtF)** - Lairs, domains, strongholds

## Directory Structure

```
locations/
├── __init__.py
├── admin.py                    # Admin configuration
├── apps.py                     # App configuration
├── forms/                      # Location creation/edit forms
│   ├── __init__.py
│   ├── core/                   # Shared form components
│   ├── vampire/                # VtM-specific forms
│   ├── werewolf/               # WtA-specific forms
│   ├── mage/                   # MtA-specific forms
│   ├── wraith/                 # WtO-specific forms
│   └── demon/                  # DtF-specific forms
├── models/                     # Location models
│   ├── __init__.py
│   ├── core/                   # Base LocationModel class
│   │   └── location.py        # Main LocationModel
│   ├── vampire/                # VtM location types
│   ├── werewolf/               # WtA location types (Caern, etc.)
│   ├── mage/                   # MtA location types (Node, Chantry)
│   ├── wraith/                 # WtO location types
│   └── demon/                  # DtF location types
├── templates/
│   └── locations/
│       ├── core/               # Base location templates
│       ├── vampire/            # VtM templates
│       ├── werewolf/           # WtA templates
│       ├── mage/               # MtA templates
│       ├── wraith/             # WtO templates
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

### Base LocationModel

All locations inherit from `LocationModel` in `models/core/location.py`:

```python
from core.models import Model

class LocationModel(Model):
    # Core fields shared across all location types
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chronicle = models.ForeignKey('game.Chronicle', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='Un')

    # Location properties
    location_type = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
```

### Gameline-Specific Locations

**Werewolf (Caern):**
```python
class Caern(LocationModel):
    # Caern-specific fields
    level = models.IntegerField(default=1)
    totem = models.CharField(max_length=100)
    tribe = models.ForeignKey('Tribe', on_delete=models.SET_NULL, null=True)
    gauntlet_rating = models.IntegerField(default=7)

    class Meta:
        verbose_name = "Caern"
        verbose_name_plural = "Caerns"
```

**Mage (Node):**
```python
class Node(LocationModel):
    # Node-specific fields
    quintessence_per_day = models.IntegerField(default=1)
    aura = models.CharField(max_length=50)
    resonance = models.CharField(max_length=100)
    sphere_affinities = models.JSONField(default=list)

    class Meta:
        verbose_name = "Node"
        verbose_name_plural = "Nodes"
```

## Usage Examples

### Creating a Caern

```python
from locations.models.werewolf import Caern

caern = Caern.objects.create(
    owner=user,
    name="Sept of the Silver Fang",
    description="Ancient caern in the mountains",
    level=3,
    totem="Falcon",
    gauntlet_rating=5
)
```

### Querying Locations

```python
# Get all locations for a user
my_locations = LocationModel.objects.filter(owner=request.user)

# Get all caerns in a chronicle
caerns = Caern.objects.filter(chronicle=chronicle)

# Get approved nodes
nodes = Node.objects.filter(status='App')
```

## Location Status

Locations follow the same status progression:

- **Un (Unfinished)** - Location in creation
- **Sub (Submitted)** - Awaiting ST approval
- **App (Approved)** - Ready for use
- **Ret (Retired)** - No longer in use
- **Dec (Deceased)** - Location destroyed

## Testing

Run location tests:
```bash
# All location tests
pytest locations/tests/

# Gameline-specific tests
pytest locations/tests/werewolf/
pytest locations/tests/mage/
```

## Permissions

Locations use standard permission checks:

- **Owner** - Can edit their own locations
- **Storyteller** - Can edit locations in their chronicles
- **Approved Status** - Only STs can approve locations

## Related Apps

- **core** - Base models and utilities
- **characters** - Locations can be associated with characters
- **game** - Locations belong to chronicles
- **accounts** - User ownership

## Common Tasks

### Adding a New Location Type

1. Create model in appropriate gameline folder
2. Create form in `forms/{gameline}/`
3. Create views in `views/{gameline}/`
4. Add URL patterns in `urls/{gameline}/`
5. Create templates in `templates/locations/{gameline}/`
6. Add tests in `tests/{gameline}/`

## Related Documentation

- See `docs/CODE_STYLE.md` for coding standards
- See `/CLAUDE.md` for project-wide conventions
- See `characters/docs/` and `items/docs/` for parallel app structures
