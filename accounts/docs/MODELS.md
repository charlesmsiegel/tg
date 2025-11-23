# Accounts App Models

User profile and authentication models for the World of Darkness RPG system.

---

## User Profile (1 model)

- **`Profile`** - User profile (one-to-one with Django User)
  - **Theme Preferences**:
    - `theme` - Site theme (dark, light, gameline-specific)
    - `preferred_heading` - Preferred gameline heading style

  - **Storyteller Status**:
    - Methods to check if user is a storyteller
    - ST relationships to chronicles
    - Gameline-specific ST permissions

  - **Approval Queues**:
    - Characters to approve
    - Items to approve
    - Locations to approve
    - XP requests to approve
    - Organized by chronicle

  - **Key Methods**:
    - `is_st()` - Check if user is a storyteller (any chronicle)
    - `is_st_for(chronicle)` - Check if ST for specific chronicle
    - `st_relations()` - Get all ST relationships
    - `objects_to_approve()` - Get approval queue items
    - `characters_to_approve()` - Characters awaiting approval
    - `items_to_approve()` - Items awaiting approval
    - `locations_to_approve()` - Locations awaiting approval
    - `rotes_to_approve()` - Mage rotes awaiting approval

---

## File Locations

- **Models:** `accounts/models.py`
- **Admin:** `accounts/admin.py` (1 model registered)
- **Views:** `accounts/views.py`
- **Forms:** `accounts/forms.py`
- **Templates:** `accounts/templates/accounts/`
- **URLs:** `accounts/urls.py`

---

## Signal Integration

Profile creation is handled via Django signals:

```python
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
```

**Location:** `accounts/models.py`
**Note:** Should be moved to `accounts/signals.py` and registered in `accounts/apps.py` per Django best practices

---

## Key Features

### Storyteller Role Management

The Profile model provides centralized ST role checking:

```python
# Check if user is a storyteller at all
if request.user.profile.is_st():
    # Show ST-only options

# Check if ST for specific chronicle
if request.user.profile.is_st_for(chronicle):
    # Allow chronicle-specific ST actions

# Get all chronicles user STs for
st_chronicles = request.user.profile.st_relations()
```

### Approval Workflow

STs can access approval queues through the profile:

```python
# Get all objects awaiting approval
approval_queue = user.profile.objects_to_approve()

# Get specific type of objects
pending_characters = user.profile.characters_to_approve()
pending_items = user.profile.items_to_approve()
pending_rotes = user.profile.rotes_to_approve()
```

### Theme Customization

Users can customize their experience:

```python
# Set preferred theme
profile.theme = 'vtm'  # Vampire theme
profile.preferred_heading = 'vtm_heading'
profile.save()

# In templates
<div class="{{ user.profile.preferred_heading }}">
    <!-- Styled with user's preferred gameline -->
</div>
```

---

## Profile Fields

| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField(User) | Django user account |
| `theme` | CharField | Site theme preference |
| `preferred_heading` | CharField | Preferred gameline heading style |

---

## Related Models

### STRelationship (game app)
- Links Profile (via User) to Chronicles
- Defines what gamelines user STs for
- Role within chronicle (Head ST, Game ST)

### WeeklyXPRequest (game app)
- ST approves/denies XP requests
- Profile methods help retrieve pending requests

### Character/Item/Location (various apps)
- All have `status` field (Un, Sub, App, Ret, Dec)
- Profile provides approval queue for items with status='Sub'

---

## Usage Patterns

### In Views
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import STRequiredMixin

class ApproveCharacterView(STRequiredMixin, UpdateView):
    # Automatically restricts to STs using profile.is_st()
    model = Character
```

### In Forms
```python
class CharacterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Show ST-only fields
        if user and user.profile.is_st():
            self.fields['npc'].widget = forms.CheckboxInput()
        else:
            del self.fields['npc']
```

### In Templates
```django
{% if user.profile.is_st %}
    <a href="{% url 'approve_characters' %}">
        Approve Characters ({{ user.profile.characters_to_approve.count }})
    </a>
{% endif %}
```

---

## Permission Integration

The Profile model integrates with the permission system:

**Role-Based Checks** (use `is_st()`):
- General ST privileges
- Form field visibility
- Template element visibility
- Non-object-specific permissions

**Object-Level Checks** (use `PermissionManager`):
- Specific character/item/location permissions
- View/edit/delete permissions
- Handled by `core.permissions.PermissionManager`

See `docs/design/permissions_system.md` for complete permission system documentation.

---

## Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| Model | ✅ | Complete |
| Admin | ✅ | Registered |
| Views | ✅ | Profile detail, update |
| Forms | ✅ | Profile update form |
| Templates | ✅ | Profile display |
| Signals | ⚠️ | Should move to signals.py |

---

## Future Enhancements

See `TODO.md` for planned improvements:
- Move signal registration to `apps.py`
- Add user preferences (notification settings, default visibility)
- Add user statistics (characters created, scenes participated in)
- Add avatar/profile picture support
- Add bio/about section
- Add favorite gameline setting

---

## See Also

- `docs/design/permissions_system.md` - Permission system design
- `docs/file_paths.md` - File path reference
- `game/MODELS.md` - STRelationship model
- `CLAUDE.md` - Coding standards
