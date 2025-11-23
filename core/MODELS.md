# Core App Models

Core shared models used across all World of Darkness gamelines.

---

## Base Polymorphic Model (1 model)

- **`Model`** - Abstract base class for all polymorphic models
  - Extends `PolymorphicModel` from django-polymorphic
  - Provides common fields: name, description
  - Base for three main inheritance trees:
    - `Character` → gameline-specific characters
    - `ItemModel` → gameline-specific items
    - `LocationModel` → gameline-specific locations
  - All subclasses inherit polymorphic behavior

---

## Source Material & References (3 models)

### Books & Documentation
- **`Book`** - Game source books
  - Name, author, publisher
  - Gameline (VtM, WtA, MtA, etc.)
  - Edition (1e, 2e, Revised, 20th Anniversary)
  - Publication year
  - ISBN
  - Used for tracking material sources

- **`BookReference`** - Page references in books
  - Book association
  - Page number(s)
  - Topic/section reference
  - Used to cite sources for game mechanics

- **`HouseRule`** - Custom house rules
  - Chronicle-specific rule modifications
  - Gameline association
  - Description of rule change
  - Applies to specific chronicle or globally
  - **Status:** Not registered in admin, no views

---

## Site Content (2 models)

- **`NewsItem`** - Site news and announcements
  - Title, content
  - Publication date
  - Author (User)
  - Visibility (public, ST-only, etc.)
  - Active/archived status

- **`Language`** - Language definitions
  - Name (English, Spanish, Latin, etc.)
  - Description
  - Used for character language skills
  - Can track modern vs. dead languages

---

## Utility Models (2 models)

> **Note:** These are helper models for specific functionality

- **`Number`** - Number/quantity helper
  - Used for tracking numeric values
  - Helper for templating and display

- **`Noun`** - Noun/term helper
  - Used for tracking game terms
  - Helper for templating and display

---

## File Locations

- **Models:** `core/models.py`
- **Admin:** `core/admin.py` (5 models registered)
- **Views:** `core/views/` (5 view files)
- **Forms:** `core/forms/`
- **Templates:** `core/templates/core/`
- **URLs:** `core/urls.py`

---

## Implementation Status

| Model | Admin | Views | Templates | Notes |
|-------|-------|-------|-----------|-------|
| Model | N/A | N/A | N/A | Abstract base class |
| Book | ✅ | ✅ | ✅ | Detail view only |
| BookReference | ✅ | ⚠️ | ⚠️ | Minimal implementation |
| HouseRule | ✅ | ❌ | ❌ | Admin only |
| NewsItem | ✅ | ✅ | ✅ | Create, update, detail |
| Language | ✅ | ✅ | ✅ | Create, update, detail |
| Number | ✅ | N/A | N/A | Utility model |
| Noun | ✅ | N/A | N/A | Utility model |

---

## Polymorphic Inheritance Trees

The `Model` base class enables three main polymorphic inheritance hierarchies:

### 1. Character Tree
```
core.models.Model (abstract)
└── characters.models.Character
    └── characters.models.Human
        ├── VtMHuman (Vampire)
        ├── WtAHuman/Werewolf (Werewolf)
        ├── MtAHuman/Mage (Mage)
        ├── WtOHuman/Wraith (Wraith)
        ├── CtDHuman/Changeling (Changeling)
        └── DtFHuman/Demon (Demon)
```

### 2. Item Tree
```
core.models.Model (abstract)
└── items.models.ItemModel
    ├── Weapon (base)
    │   ├── MeleeWeapon
    │   ├── RangedWeapon
    │   └── ThrownWeapon
    ├── Material
    ├── Medium
    └── [Gameline-specific items]
        ├── Artifact (Mage)
        ├── Wonder (Mage)
        ├── Fetish (Werewolf)
        ├── Talen (Werewolf)
        └── etc.
```

### 3. Location Tree
```
core.models.Model (abstract)
└── locations.models.LocationModel
    ├── City (general)
    ├── Node (Mage)
    ├── Chantry (Mage)
    ├── Caern (Werewolf)
    └── etc.
```

---

## Key Features

### Polymorphic Queries
The polymorphic base enables querying all subclasses:

```python
# Get all characters across all gamelines
all_characters = Character.objects.all()

# Get specific gameline
vampires = Character.objects.instance_of(VtMHuman)

# Get base type
items = ItemModel.objects.all()  # Returns all items, all types
```

### Gameline Tracking
Models track their gameline affiliation:
- Books specify which gameline they belong to
- House rules can apply to specific gamelines or all
- Languages can be gameline-specific or universal

### Source Documentation
- `Book` + `BookReference` provide citation system
- Tracks which mechanics come from which books
- Useful for rule verification and official material tracking

---

## Common Patterns

### Book Usage
```python
# Create a book
vtm_corebook = Book.objects.create(
    name="Vampire: The Masquerade (Revised)",
    gameline="vtm",
    edition="Rev",
    publisher="White Wolf"
)

# Reference a page
ref = BookReference.objects.create(
    book=vtm_corebook,
    page_number=129,
    topic="Disciplines: Celerity"
)
```

### House Rules
```python
# Create chronicle-specific house rule
rule = HouseRule.objects.create(
    name="Modified Willpower",
    gameline="all",
    description="Willpower regenerates 1 per scene instead of per session",
    chronicle=my_chronicle
)
```

### Site News
```python
# Post site news
news = NewsItem.objects.create(
    title="New Mage Content Available",
    content="Added 20 new Paradigms and Practices",
    author=request.user
)
```

---

## See Also

- `docs/models/implementation_status.md` - Full implementation details
- `docs/file_paths.md` - File path reference
- `CLAUDE.md` - Coding standards, polymorphic pattern usage
