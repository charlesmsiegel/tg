# Items App

The `items` app manages equipment, artifacts, and magical items across all World of Darkness gamelines. Like the characters app, it uses polymorphic inheritance to support gameline-specific item types while sharing common functionality.

## Purpose

The items app provides:
- Item creation and management for all WoD gamelines
- Polymorphic item models (weapons, armor, fetishes, talismans, etc.)
- Gameline-specific magical and mundane items
- Item ownership and chronicle association
- Item status management (Unfinished → Submitted → Approved)
- Gameline-specific forms, views, and templates

## Supported Item Types

- **Vampire (VtM)** - Weapons, armor, blood bags, ritual components
- **Werewolf (WtA)** - Fetishes, talismans, klaives, caern items
- **Mage (MtA)** - Wonders, talismans, grimoires, nodes (as items)
- **Wraith (WtO)** - Relics, artifacts, fetters
- **Changeling (CtD)** - Treasures, chimera, tokens
- **Demon (DtF)** - Relics, infernal items

## Directory Structure

```
items/
├── __init__.py
├── admin.py                    # Admin configuration
├── apps.py                     # App configuration
├── forms/                      # Item creation/edit forms
│   ├── __init__.py
│   ├── core/                   # Shared form components
│   ├── vampire/                # VtM-specific forms
│   ├── werewolf/               # WtA-specific forms
│   ├── mage/                   # MtA-specific forms
│   ├── wraith/                 # WtO-specific forms
│   ├── changeling/             # CtD-specific forms
│   └── demon/                  # DtF-specific forms
├── models/                     # Item models
│   ├── __init__.py
│   ├── core/                   # Base ItemModel class
│   │   ├── item.py            # Main ItemModel
│   │   └── weapon.py          # Generic weapon stats
│   ├── vampire/                # VtM item types
│   ├── werewolf/               # WtA item types (Fetish, etc.)
│   ├── mage/                   # MtA item types (Wonder, etc.)
│   ├── wraith/                 # WtO item types
│   ├── changeling/             # CtD item types
│   └── demon/                  # DtF item types
├── templates/
│   └── items/
│       ├── core/               # Base item templates
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

### Base ItemModel

All items inherit from `ItemModel` in `models/core/item.py`:

```python
from core.models import Model

class ItemModel(Model):
    # Core fields shared across all item types
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    chronicle = models.ForeignKey('game.Chronicle', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='Un')

    # Basic properties
    item_type = models.CharField(max_length=50)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    value = models.IntegerField(default=0)  # In Resources dots

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
```

### Gameline-Specific Items

**Werewolf (Fetish):**
```python
class Fetish(ItemModel):
    # Werewolf-specific fields
    gnosis = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    spirit_type = models.CharField(max_length=100)
    power = models.TextField()

    class Meta:
        verbose_name = "Fetish"
        verbose_name_plural = "Fetishes"
```

**Mage (Wonder):**
```python
class Wonder(ItemModel):
    # Mage-specific fields
    arete = models.IntegerField(default=1)
    quintessence = models.IntegerField(default=0)
    paradox = models.IntegerField(default=0)
    sphere_requirements = models.JSONField(default=dict)
    effects = models.TextField()

    class Meta:
        verbose_name = "Wonder"
        verbose_name_plural = "Wonders"
```

## Usage Examples

### Creating a Fetish

```python
from items.models.werewolf import Fetish

fetish = Fetish.objects.create(
    owner=user,
    name="Spirit Whistle",
    description="A bone whistle that summons spirits",
    gnosis=5,
    level=2,
    spirit_type="Wind Spirit",
    power="Summons a wind spirit when blown"
)
```

### Querying Items

```python
# Get all items for a user
my_items = ItemModel.objects.filter(owner=request.user)

# Get all fetishes in a chronicle
fetishes = Fetish.objects.filter(chronicle=chronicle)

# Get approved wonders
wonders = Wonder.objects.filter(status='App')
```

## Item Status

Items follow the same status progression as characters:

- **Un (Unfinished)** - Item in creation
- **Sub (Submitted)** - Awaiting ST approval
- **App (Approved)** - Ready for use
- **Ret (Retired)** - No longer in use
- **Dec (Deceased)** - Item destroyed

## Testing

Run item tests:
```bash
# All item tests
pytest items/tests/

# Gameline-specific tests
pytest items/tests/werewolf/
pytest items/tests/mage/

# Specific test file
pytest -v items/tests/werewolf/test_fetish.py
```

## Permissions

Items use these permission checks:

- **Owner** - Can edit their own items
- **Storyteller** - Can edit items in their chronicles
- **Approved Status** - Only STs can approve items

## Related Apps

- **core** - Base models and utilities
- **characters** - Items can be assigned to characters
- **game** - Items belong to chronicles
- **accounts** - User ownership

## Common Tasks

### Adding a New Item Type

1. Create model in appropriate gameline folder
2. Create form in `forms/{gameline}/`
3. Create views in `views/{gameline}/`
4. Add URL patterns in `urls/{gameline}/`
5. Create templates in `templates/items/{gameline}/`
6. Add tests in `tests/{gameline}/`

### Adding a New Property

1. Add field to appropriate model
2. Create migration: `python manage.py makemigrations`
3. Update form to include new field
4. Update template to display property
5. Add tests for the new property

## Related Documentation

- See `docs/CODE_STYLE.md` for coding standards
- See `docs/MODELS.md` for model patterns
- See `/CLAUDE.md` for project-wide conventions
- See `characters/docs/` for parallel character app structure
