# Game App

The `game` app manages chronicles (campaigns), game sessions, stories, and experience point (XP) tracking. It provides the organizational structure for running World of Darkness games.

## Purpose

The game app provides:
- Chronicle (campaign) creation and management
- Scene (game session) tracking
- Story arcs grouping multiple scenes
- XP award and approval workflows
- Weekly XP requests
- Storyteller-player relationships
- Journal entries for recording game events

## Key Components

### Chronicle

The central organizational unit representing a campaign or ongoing game.

```python
class Chronicle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    gameline = models.CharField(max_length=20)

    # Participants
    storytellers = models.ManyToManyField(User, related_name='st_chronicles')
    players = models.ManyToManyField(User, related_name='player_chronicles')

    # Settings
    allowed_books = models.ManyToManyField('core.Book')
    house_rules = models.ManyToManyField('core.HouseRule')

    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='Un')
```

**Key Features:**
- Multiple storytellers supported
- Gameline-specific (can't mix VtM and WtA in one chronicle)
- Book and house rule management
- Player roster tracking

### Scene

Represents a single game session.

```python
class Scene(models.Model):
    name = models.CharField(max_length=100)
    chronicle = models.ForeignKey(Chronicle, on_delete=models.CASCADE)
    story = models.ForeignKey('Story', on_delete=models.SET_NULL, null=True, blank=True)

    # Session details
    date = models.DateField()
    description = models.TextField()

    # Participants
    characters = models.ManyToManyField('characters.Character')

    # XP awarded
    base_xp = models.IntegerField(default=1)
    bonus_xp = models.IntegerField(default=0)
```

**Key Features:**
- Associated with a chronicle and optional story arc
- Tracks which characters participated
- XP awards (base + bonus)
- Session date and description

### Story

Groups related scenes into story arcs.

```python
class Story(models.Model):
    name = models.CharField(max_length=100)
    chronicle = models.ForeignKey(Chronicle, on_delete=models.CASCADE)
    description = models.TextField()

    # Story tracking
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20)
```

### Week

Represents a week in chronicle time (not real-world time).

```python
class Week(models.Model):
    chronicle = models.ForeignKey(Chronicle, on_delete=models.CASCADE)
    week_number = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    # XP tracking
    xp_awarded = models.IntegerField(default=0)
```

### WeeklyXPRequest

Tracks character XP spending requests that require ST approval.

```python
class WeeklyXPRequest(models.Model):
    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)

    # XP spending
    trait = models.CharField(max_length=100)
    cost = models.IntegerField()
    notes = models.TextField(blank=True)

    # Approval
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
```

### Journal

In-character or out-of-character session notes.

```python
class Journal(models.Model):
    character = models.ForeignKey('characters.Character', on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=200)
    content = models.TextField()
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
```

## Directory Structure

```
game/
├── __init__.py
├── admin.py                    # Admin configuration
├── apps.py                     # App configuration
├── forms.py                    # Forms for all game models
├── models.py                   # All game models (Chronicle, Scene, etc.)
├── signals.py                  # Signal handlers
├── templates/
│   └── game/
│       ├── chronicle/          # Chronicle templates
│       │   ├── detail.html
│       │   ├── create.html
│       │   └── list.html
│       ├── scene/              # Scene templates
│       ├── story/              # Story templates
│       └── journal/            # Journal templates
├── tests.py                    # Unit tests
├── tests_integration.py        # Integration tests
├── urls.py                     # URL routing
└── views.py                    # All views
```

## Usage Examples

### Creating a Chronicle

```python
from game.models import Chronicle

chronicle = Chronicle.objects.create(
    name="Blood and Shadows",
    description="Vampire chronicle in modern Seattle",
    gameline='vtm'
)

# Add storyteller and players
chronicle.storytellers.add(st_user)
chronicle.players.add(player1, player2, player3)
```

### Recording a Game Session

```python
from game.models import Scene

scene = Scene.objects.create(
    name="The Elysium Gathering",
    chronicle=chronicle,
    date=datetime.date.today(),
    description="First meeting with the Prince",
    base_xp=1,
    bonus_xp=1  # For good roleplay
)

# Add participating characters
scene.characters.add(character1, character2, character3)

# XP is automatically awarded to characters via signals
```

### XP Approval Workflow

```python
# Player submits XP spending request
request = WeeklyXPRequest.objects.create(
    character=my_character,
    week=current_week,
    trait="Celerity 2",
    cost=10,
    notes="Advancing Discipline"
)

# Storyteller reviews and approves
request.approved = True
request.approved_by = st_user
request.save()

# Character's XP is automatically deducted via signals
```

### Querying Game Data

```python
# Get all chronicles a user is involved in
my_chronicles = Chronicle.objects.filter(
    Q(storytellers=user) | Q(players=user)
)

# Get all scenes in a chronicle
scenes = Scene.objects.filter(chronicle=chronicle).order_by('-date')

# Get XP requests needing approval
pending_requests = WeeklyXPRequest.objects.filter(
    character__chronicle=chronicle,
    approved=False
)
```

## XP System

### Earning XP

1. ST creates a Scene
2. ST adds participating characters
3. ST sets base_xp (typically 1) and bonus_xp (0-2)
4. When scene is saved, XP is automatically awarded to characters

### Spending XP

1. Player creates WeeklyXPRequest for desired advancement
2. Request is marked as pending (approved=False)
3. ST reviews request in approval queue
4. ST approves or rejects request
5. If approved, XP is deducted from character automatically

### XP Costs

XP costs are defined in character advancement rules and vary by gameline:

- Attributes: new rating × 4
- Abilities: new rating × 2
- Disciplines/Gifts/Spheres: new rating × 7 (current rating × 5 for Clan Disciplines)
- Willpower: current rating × 1
- Backgrounds: new rating × 3

## Testing

Run game app tests:
```bash
# All game tests
pytest game/tests.py

# Integration tests
pytest game/tests_integration.py

# Specific test
pytest -v game/tests.py::ChronicleTestCase
```

## Signals

The game app uses Django signals for automatic XP processing:

- **post_save on Scene** - Awards XP to participating characters
- **post_save on WeeklyXPRequest** - Deducts XP when approved

## Permissions

### Chronicle Permissions

- **Storyteller** - Full access to chronicle, can approve XP, add/remove players
- **Player** - Can view chronicle, create characters, submit XP requests
- **Public** - Can view if chronicle is public

### Scene Permissions

- **Storyteller** - Can create/edit scenes
- **Player** - Can view scenes their characters participated in
- **Public** - No access to scenes

## Related Apps

- **accounts** - User profiles, ST relationships
- **characters** - Characters belong to chronicles
- **core** - Books and house rules for chronicles

## Common Tasks

### Starting a New Chronicle

1. Create Chronicle with name, description, gameline
2. Add storytellers and players
3. Select allowed source books
4. Add house rules if needed
5. Set status to 'App' (Approved) when ready

### Running a Game Session

1. Create Scene with date and description
2. Add participating characters
3. Set XP awards (base + bonus)
4. Add journal entries for recap
5. Process XP spending requests

## Related Documentation

- See `docs/CODE_STYLE.md` for coding standards
- See `docs/XP_SYSTEM.md` for detailed XP rules
- See `/CLAUDE.md` for project-wide conventions
