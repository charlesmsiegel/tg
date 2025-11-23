# Django Messages Framework Implementation Guide

This guide documents the comprehensive messaging framework implemented across the application to provide user feedback for all actions.

## Overview

The application now uses Django's built-in messages framework to provide real-time feedback to users for:
- Form submissions (success and failure)
- Character creation and approval workflows
- Scene and story management
- XP requests and approvals
- Permission errors
- All CRUD operations

## Implementation

### 1. Base Template Update

**Location:** `core/templates/core/base.html`

The base template now displays messages prominently after the navbar:

```html
<!-- Message Display Area -->
{% if messages %}
    {% load sanitize_text %}
    <div class="container mt-3">
        {% for message in messages %}
            <div class="tg-message {{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message|sanitize_html }}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        {% endfor %}
    </div>
{% endif %}
```

**Styling:** Messages use existing TG styles defined in `staticfiles/themes/components.css`:
- `.tg-message.success` - Green success messages
- `.tg-message.error` - Red error messages
- `.tg-message.warning` - Yellow warning messages
- `.tg-message.info` - Blue informational messages

### 2. Reusable Message Mixins

**Location:** `core/views/message_mixin.py`

Three reusable mixins have been created:

#### SuccessMessageMixin
Adds success messages to CreateView/UpdateView:

```python
from core.views.message_mixin import SuccessMessageMixin

class VampireCreateView(SuccessMessageMixin, CreateView):
    model = Vampire
    success_message = "Vampire '{name}' created successfully!"
```

#### ErrorMessageMixin
Adds error messages when form validation fails:

```python
from core.views.message_mixin import ErrorMessageMixin

class MyView(ErrorMessageMixin, CreateView):
    error_message = "Please correct the errors below."
```

#### MessageMixin
Combined mixin for both success and error:

```python
from core.views.message_mixin import MessageMixin

class VampireCreateView(MessageMixin, CreateView):
    model = Vampire
    success_message = "Vampire '{name}' created successfully!"
    error_message = "Failed to create vampire. Please correct the errors below."
```

**Message Formatting:**
- Use `{name}`, `{id}`, `{pk}` in messages to insert object values
- Example: `"Character '{name}' approved successfully!"` → `"Character 'Alucard' approved successfully!"`

### 3. Implemented Views

The following views have been updated with comprehensive messaging:

#### Characters
- `characters/views/vampire/vampire_chargen.py`
  - `VampireBasicsView` - Character creation success/error
  - `VampireDisciplinesView` - Discipline allocation validation with specific error messages
  - `VampireVirtuesView` - Virtue allocation validation
  - `VampireExtrasView` - Details saved confirmation
- `characters/views/vampire/vampire.py`
  - `VampireCreateView` - Creation success/error
  - `VampireUpdateView` - Update success/error

#### Game
- `game/views.py`
  - `ChronicleDetailView` - Story/scene creation success
  - `SceneDetailView` - Scene closure, character addition, post creation
  - `JournalDetailView` - Journal entry and ST response success/error
  - `StoryCreateView` - Story creation
  - `StoryUpdateView` - Story updates

#### Accounts
- `accounts/views.py`
  - `SignUp` - Account creation success
  - `CustomLoginView` - Login welcome message and error
  - `ProfileView` - All approval actions (characters, locations, items, rotes, images, XP requests)
  - `ProfileUpdateView` - Profile update success

## Message Categories

### Success Messages
Used for successful operations:
```python
messages.success(request, "Character created successfully!")
```

### Error Messages
Used for validation failures and errors:
```python
messages.error(request, "You must spend exactly 3 dots on Disciplines.")
```

### Warning Messages
Used for non-critical issues:
```python
messages.warning(request, "This action cannot be undone.")
```

### Info Messages
Used for informational feedback:
```python
messages.info(request, "Character submitted for approval.")
```

## Character Creation Error Messages

Character creation now provides specific error messages for common validation failures:

### Discipline Allocation
- "Discipline allocation error: You must spend exactly 3 dots. You have {total}."
- "You can only allocate starting dots to your clan's Disciplines."

### Virtue Allocation
- "Virtue allocation error: You must spend exactly 7 dots. You have {total}."

### Attribute Allocation
Inherited from HumanAttributeView - validates primary/secondary/tertiary allocation

### Ability Allocation
Inherited from VtMHumanAbilityView - validates 13/9/5 point distribution

## Permission Error Messages

All permission-protected actions now show friendly error messages before raising PermissionDenied:

```python
if not request.user.profile.is_st():
    messages.error(request, "Only storytellers can create stories and scenes.")
    raise PermissionDenied("Only storytellers can create stories and scenes")
```

## Approval Workflow Messages

The ProfileView now provides detailed feedback for all approval actions:

- **Character Approval:** "Character '{name}' approved successfully!"
- **Location Approval:** "Location '{name}' approved successfully!"
- **Item Approval:** "Item '{name}' approved successfully!"
- **Rote Approval:** "Rote '{name}' approved successfully!"
- **Image Approval:** "Image for '{name}' approved successfully!"
- **XP Awards:** "XP awarded for scene '{name}'!"
- **Freebie Awards:** "Freebies awarded to '{name}'!"
- **Weekly XP Requests:** "Weekly XP request submitted for '{name}'!"
- **Weekly XP Approvals:** "Weekly XP request approved for '{name}'!"

## Adding Messages to New Views

### For Class-Based Views (Recommended)

Use the appropriate mixin:

```python
from core.views.message_mixin import MessageMixin
from django.views.generic import CreateView

class MyCreateView(MessageMixin, CreateView):
    model = MyModel
    fields = ['name', 'description']
    success_message = "{model_name} '{name}' created successfully!"
    error_message = "Failed to create {model_name}. Please correct the errors below."
```

### For Function-Based Views

Use Django messages directly:

```python
from django.contrib import messages

def my_view(request):
    if form.is_valid():
        form.save()
        messages.success(request, "Operation completed successfully!")
        return redirect('success_url')
    else:
        messages.error(request, "Please correct the errors below.")
        return render(request, 'template.html', {'form': form})
```

### For Custom Validation

Add specific messages before returning form_invalid:

```python
def form_valid(self, form):
    if some_condition_fails:
        form.add_error(None, "Technical error message for form")
        messages.error(self.request, "User-friendly error message")
        return self.form_invalid(form)

    # Proceed with save
    messages.success(self.request, "Operation successful!")
    return super().form_valid(form)
```

## Extending to Remaining Views

The following view types should be updated with messages as needed:

### High Priority
1. **Character Creation Views** - All gamelines (Mage, Werewolf, Changeling, Wraith, Demon)
2. **Item CRUD Views** - Wonders, Fetishes, Talismans, etc.
3. **Location CRUD Views** - Chantries, Nodes, Havens, Caerns, etc.

### Medium Priority
1. **Specialty Views** - Rotes, Gifts, Rites, Arts, Edges
2. **Background Views** - Adding/editing backgrounds
3. **MeritFlaw Views** - Adding merits and flaws

### Pattern for Standard CRUD Views

For simple CreateView/UpdateView/DeleteView classes, add the MessageMixin:

```python
# Before
class MyCreateView(CreateView):
    model = MyModel
    fields = [...]

# After
from core.views.message_mixin import MessageMixin

class MyCreateView(MessageMixin, CreateView):
    model = MyModel
    fields = [...]
    success_message = "{model_name} '{name}' created successfully!"
    error_message = "Failed to create {model_name}. Please correct the errors below."
```

## Testing Messages

### Manual Testing
1. Perform an action (create character, approve item, etc.)
2. Verify message appears at top of page
3. Verify message is dismissible
4. Verify message styling matches action type (success=green, error=red)

### Automated Testing (Future)
```python
from django.contrib.messages import get_messages

def test_character_creation_success_message(self):
    response = self.client.post('/characters/vampire/create/', data={...})
    messages = list(get_messages(response.wsgi_request))
    self.assertEqual(len(messages), 1)
    self.assertEqual(str(messages[0]), "Vampire 'Test' created successfully!")
    self.assertEqual(messages[0].tags, 'success')
```

## Best Practices

1. **Be Specific:** Use object names in messages when possible
   - Good: "Character 'Alucard' approved successfully!"
   - Bad: "Object approved."

2. **Be Consistent:** Use similar phrasing across similar actions
   - Creation: "{type} '{name}' created successfully!"
   - Update: "{type} '{name}' updated successfully!"
   - Deletion: "{type} '{name}' deleted successfully!"
   - Approval: "{type} '{name}' approved successfully!"

3. **Provide Context for Errors:** Help users understand what went wrong
   - Good: "You must spend exactly 3 dots on Disciplines. You have 4."
   - Bad: "Invalid input."

4. **Use Appropriate Message Levels:**
   - `success` - Action completed successfully
   - `error` - Action failed or validation error
   - `warning` - Proceed with caution
   - `info` - FYI, no action needed

5. **Security:** Never include sensitive information in messages (passwords, tokens, etc.)

6. **Accessibility:** Messages are automatically announced to screen readers via `role="alert"`

## Future Enhancements

1. **Message Persistence:** Store critical messages in database for notification history
2. **Toast Notifications:** Add AJAX-based toast notifications for non-page-reload actions
3. **Message Categories:** Group related messages (e.g., "3 characters approved")
4. **Undo Actions:** Add "Undo" links to certain message types
5. **Email Notifications:** Send email for critical messages (character approved, XP awarded)
6. **Message Templates:** Create message templates for common phrases
7. **Internationalization:** Add translation support for messages

## Troubleshooting

### Messages Not Appearing
1. Check that `django.contrib.messages` is in `INSTALLED_APPS`
2. Check that `MessageMiddleware` is in `MIDDLEWARE`
3. Verify `context_processors` includes `django.contrib.messages.context_processors.messages`
4. Check that view is redirecting after message (messages persist across redirects)

### Messages Appearing Multiple Times
- Don't call `messages.add()` multiple times for same action
- Check that form_valid doesn't call both parent and add message twice

### Styling Issues
- Verify Bootstrap CSS is loaded
- Check that TG component styles are loaded after Bootstrap
- Verify message tags match CSS classes (success, error, warning, info)

## Additional Resources

- [Django Messages Framework Docs](https://docs.djangoproject.com/en/5.1/ref/contrib/messages/)
- [Bootstrap Alerts](https://getbootstrap.com/docs/5.1/components/alerts/)
- Project: `SOURCES/STYLE.md` for TG styling conventions
