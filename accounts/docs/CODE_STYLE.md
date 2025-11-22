# Accounts App - Code Style Guide

## Overview

The accounts app manages user profiles and authentication. It extends Django's User model and provides storyteller-specific functionality.

## General Principles

1. **Extend, Don't Replace** - Use Profile model to extend User, don't create custom User
2. **Signal-Driven** - Auto-create profiles on user creation
3. **Permission-Aware** - Clear distinction between players and storytellers
4. **Secure by Default** - Follow Django security best practices

## Model Patterns

### Profile Model

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """User profile with WoD-specific preferences."""

    # One-to-one with User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    # Preferences
    theme = models.CharField(
        max_length=20,
        choices=[
            ('dark', 'Dark'),
            ('light', 'Light'),
            ('vtm', 'Vampire'),
            ('wta', 'Werewolf'),
            ('mta', 'Mage'),
        ],
        default='dark'
    )
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # ST status
    is_storyteller = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"Profile for {self.user.username}"

    def is_st(self):
        """Check if user is a storyteller."""
        return self.is_storyteller

    def st_relations(self):
        """Get chronicles where user is ST."""
        return self.user.st_chronicles.all()

    def get_characters(self):
        """Get user's characters."""
        return self.user.characters.all()
```

**Best Practices:**
- Always use OneToOneField to User
- Use related_name='profile' for easy access
- Provide helper methods for common queries
- Store preferences, not core user data

### Signal Handlers

```python
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile when user is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

**Best Practices:**
- Always create profile on user creation
- Check for profile existence before accessing
- Keep signals simple and focused

## Form Patterns

### Registration Form

```python
# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    """User registration form with email."""

    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address."
    )
    display_name = forms.CharField(
        max_length=100,
        required=False,
        help_text="Optional. How you want to be displayed to others."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        """Save user and set profile fields."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Profile created via signal
            if self.cleaned_data.get('display_name'):
                user.profile.display_name = self.cleaned_data['display_name']
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
            'theme': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
```

## View Patterns

### Dashboard View

```python
# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from characters.models import Character
from game.models import Chronicle

@login_required
def dashboard(request):
    """User dashboard showing characters and chronicles."""
    profile = request.user.profile

    context = {
        'profile': profile,
        'my_characters': Character.objects.filter(owner=request.user),
        'my_chronicles': Chronicle.objects.filter(players=request.user),
    }

    # Add ST-specific context
    if profile.is_st():
        context['st_chronicles'] = Chronicle.objects.filter(
            storytellers=request.user
        )
        context['pending_characters'] = Character.objects.filter(
            chronicle__storytellers=request.user,
            status='Sub'
        )

    return render(request, 'accounts/dashboard.html', context)
```

### Profile Edit View

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import Profile
from .forms import ProfileForm

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Edit user profile."""
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self):
        """Get current user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Redirect to profile page."""
        return reverse('accounts:profile')
```

## Context Processors

```python
# context_processors.py
def user_context(request):
    """Add user profile to all templates."""
    context = {}

    if request.user.is_authenticated:
        context['user_profile'] = request.user.profile
        context['user_theme'] = request.user.profile.theme
        context['is_st'] = request.user.profile.is_st()

    return context
```

Add to settings.py:
```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... other processors
                'accounts.context_processors.user_context',
            ],
        },
    },
]
```

## Template Patterns

### Dashboard Template

```html
<!-- templates/accounts/dashboard.html -->
{% extends "core/base.html" %}

{% block content %}
<div class="container">
    <h1>Dashboard</h1>

    <div class="row">
        <div class="col-md-6">
            <div class="tg-card">
                <div class="tg-card-header">
                    <h5>My Characters</h5>
                </div>
                <div class="tg-card-body">
                    {% for character in my_characters %}
                        <a href="{{ character.get_absolute_url }}">
                            {{ character.name }}
                        </a>
                    {% empty %}
                        <p>No characters yet.</p>
                    {% endfor %}
                </div>
            </div>
        </div>

        {% if is_st %}
            <div class="col-md-6">
                <div class="tg-card">
                    <div class="tg-card-header">
                        <h5>Approval Queue</h5>
                    </div>
                    <div class="tg-card-body">
                        {% for character in pending_characters %}
                            <a href="{{ character.get_absolute_url }}">
                                {{ character.name }}
                            </a>
                        {% empty %}
                            <p>No pending approvals.</p>
                        {% endfor %}
                    </div>
                </div>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

## Testing Patterns

```python
# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile

class ProfileTestCase(TestCase):
    """Tests for Profile model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    def test_profile_auto_created(self):
        """Test profile is auto-created on user creation."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsNotNone(self.user.profile)

    def test_is_st_default_false(self):
        """Test is_st() defaults to False."""
        self.assertFalse(self.user.profile.is_st())

    def test_is_st_when_true(self):
        """Test is_st() when storyteller."""
        self.user.profile.is_storyteller = True
        self.user.profile.save()
        self.assertTrue(self.user.profile.is_st())
```

## URL Patterns

```python
# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),

    # ST functions
    path('approval-queue/', views.approval_queue, name='approval_queue'),
]
```

## Best Practices

- Always check if user is authenticated before accessing profile
- Use `@login_required` decorator for profile-related views
- Store only user preferences in Profile, not core app data
- Use signals to ensure profile always exists
- Provide clear user feedback on registration/login

## Anti-Patterns to Avoid

- ❌ Creating custom User model (use Profile instead)
- ❌ Accessing profile without checking existence
- ❌ Storing character/chronicle data in Profile
- ❌ Allowing users to self-assign ST status
- ❌ Skipping email validation

## Security Best Practices

- Use Django's built-in password hashing
- Require email confirmation for registration (optional)
- Implement rate limiting on login attempts
- Use HTTPS in production
- Set secure session cookies

## See Also

- Django Authentication Documentation
- `/CLAUDE.md` - Project-wide conventions
- `game/docs/CODE_STYLE.md` - Chronicle and ST relationships
