# Accounts App

The `accounts` app manages user profiles, authentication, storyteller relationships, and user preferences. It extends Django's built-in User model with additional World of Darkness-specific functionality.

## Purpose

The accounts app provides:
- User registration and authentication
- User profiles with preferences (theme, display settings)
- Storyteller status and relationships
- Approval queues for STs
- User dashboard
- Profile management

## Key Components

### Profile Model

Extends Django's User model with a one-to-one relationship:

```python
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Theme preferences
    theme = models.CharField(max_length=20, default='dark')

    # Storyteller status
    is_storyteller = models.BooleanField(default=False)

    # Other preferences
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def is_st(self):
        """Check if user is a storyteller."""
        return self.is_storyteller

    def st_relations(self):
        """Get all chronicles where user is ST."""
        return self.user.st_chronicles.all()

    def objects_to_approve(self):
        """Get all objects requiring ST approval."""
        # Characters, items, locations, XP requests
        pass
```

### Key Methods

**Profile Methods:**
- `is_st()` - Check if user is a storyteller
- `st_relations()` - Get chronicles where user is ST
- `objects_to_approve()` - Get approval queue for ST
- `get_characters()` - Get user's characters
- `get_chronicles()` - Get chronicles user is involved in

## Directory Structure

```
accounts/
├── __init__.py
├── admin.py                    # Admin configuration
├── apps.py                     # App configuration
├── context_processors.py       # Global context (user profile, theme)
├── forms.py                    # Registration, profile edit forms
├── models.py                   # Profile model
├── signals.py                  # Auto-create profile on user creation
├── templates/
│   └── accounts/
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── dashboard.html
│       └── approval_queue.html
├── tests.py                    # Unit tests
├── tests_integration.py        # Integration tests
├── urls.py                     # URL routing
└── views.py                    # Authentication and profile views
```

## Usage Examples

### User Registration

```python
from django.contrib.auth.models import User
from accounts.models import Profile

# User created via registration form
user = User.objects.create_user(
    username='player1',
    email='player1@example.com',
    password='securepassword'
)

# Profile automatically created via signal
profile = user.profile
profile.display_name = "Player One"
profile.theme = 'dark'
profile.save()
```

### Checking ST Status

```python
# In views
if request.user.profile.is_st():
    # Show ST controls
    pass

# In templates
{% if request.user.profile.is_st %}
    <a href="{% url 'accounts:approval_queue' %}">Approval Queue</a>
{% endif %}
```

### Approval Queue

```python
# Get all objects requiring approval
def approval_queue(request):
    if not request.user.profile.is_st():
        raise PermissionDenied

    # Characters needing approval
    characters = Character.objects.filter(
        chronicle__storytellers=request.user,
        status='Sub'
    )

    # XP requests needing approval
    xp_requests = WeeklyXPRequest.objects.filter(
        character__chronicle__storytellers=request.user,
        approved=False
    )

    return render(request, 'accounts/approval_queue.html', {
        'characters': characters,
        'xp_requests': xp_requests,
    })
```

## Authentication Flow

### Registration

1. User fills out registration form
2. User account created
3. Profile automatically created via signal
4. User logged in automatically
5. Redirected to dashboard

### Login

1. User enters username/password
2. Django authenticates user
3. Session created
4. Redirected to dashboard or previous page

## Context Processors

The accounts app provides global context available in all templates:

```python
# context_processors.py
def user_context(request):
    """Add user profile and preferences to all templates."""
    context = {}

    if request.user.is_authenticated:
        context['user_profile'] = request.user.profile
        context['user_theme'] = request.user.profile.theme
        context['is_st'] = request.user.profile.is_st()

    return context
```

## Signals

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

## Testing

Run accounts tests:
```bash
# All accounts tests
pytest accounts/tests.py

# Integration tests
pytest accounts/tests_integration.py

# Specific test
pytest -v accounts/tests.py::ProfileTestCase
```

## Permissions

### User Levels

1. **Anonymous** - Can view public content only
2. **Player** - Can create characters, join chronicles
3. **Storyteller** - Can create chronicles, approve characters/XP
4. **Superuser** - Full access to all content

### Permission Helpers

```python
def user_can_edit_object(user, obj):
    """Check if user can edit an object."""
    if user.is_superuser:
        return True
    if hasattr(obj, 'owner') and obj.owner == user:
        return True
    if hasattr(obj, 'chronicle') and obj.chronicle:
        if obj.chronicle.storytellers.filter(id=user.id).exists():
            return True
    return False
```

## Dashboard

The user dashboard shows:

- **For All Users:**
  - My characters
  - My chronicles (as player)
  - Recent activity

- **For Storytellers:**
  - Chronicles I run
  - Approval queue (characters, XP requests)
  - Player statistics

## Forms

### Registration Form

```python
# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    """Extended registration form."""
    email = forms.EmailField(required=True)
    display_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Profile auto-created via signal
            user.profile.display_name = self.cleaned_data.get('display_name', '')
            user.profile.save()
        return user
```

### Profile Edit Form

```python
class ProfileForm(forms.ModelForm):
    """Form for editing user profile."""

    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'avatar', 'theme']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
```

## Views

### Dashboard View

```python
# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    """User dashboard."""
    profile = request.user.profile

    context = {
        'my_characters': Character.objects.filter(owner=request.user),
        'my_chronicles': Chronicle.objects.filter(players=request.user),
    }

    if profile.is_st():
        context['st_chronicles'] = Chronicle.objects.filter(storytellers=request.user)
        context['pending_approvals'] = profile.objects_to_approve()

    return render(request, 'accounts/dashboard.html', context)
```

## Theme System

Users can select from multiple themes:

- **Dark** - Dark theme (default)
- **Light** - Light theme
- **VtM** - Vampire-themed
- **WtA** - Werewolf-themed
- **MtA** - Mage-themed

Theme preference is stored in profile and applied via CSS classes.

## Related Apps

- **core** - Base models and utilities
- **game** - Chronicles and storyteller relationships
- **characters** - Character ownership

## Common Tasks

### Making a User a Storyteller

```python
user.profile.is_storyteller = True
user.profile.save()
```

### Changing User Theme

```python
user.profile.theme = 'vtm'
user.profile.save()
```

### Getting User's Approval Queue

```python
pending_items = user.profile.objects_to_approve()
```

## Security Considerations

- Passwords are hashed using Django's default PBKDF2 algorithm
- Sessions expire after inactivity
- Profile data is validated before saving
- ST status cannot be self-assigned (requires admin)

## Related Documentation

- See `docs/CODE_STYLE.md` for coding standards
- See `docs/PERMISSIONS.md` for permission system details
- See `/CLAUDE.md` for project-wide conventions
