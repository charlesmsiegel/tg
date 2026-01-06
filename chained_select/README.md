# Django Chained Select

Self-contained cascading dropdown fields that work like native Django form fields. Just render the field - nothing else needed.

## Installation

1. Copy the `chained_select` folder into your Django project
2. Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'chained_select',
]
```

That's it.

## Quick Start - Static Choices

```python
# forms.py
from django import forms
from chained_select import ChainedChoiceField, ChainedSelectMixin

class LocationForm(ChainedSelectMixin, forms.Form):
    country = ChainedChoiceField(
        choices=[('us', 'United States'), ('ca', 'Canada')],
        empty_label="Select country..."
    )
    
    state = ChainedChoiceField(
        parent_field='country',
        empty_label="Select state/province...",
        choices_map={
            'us': [('ca', 'California'), ('ny', 'New York'), ('tx', 'Texas')],
            'ca': [('on', 'Ontario'), ('bc', 'British Columbia')],
        }
    )
```

```html
<!-- template.html - That's really all you need -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

No `{{ form.media }}`. No JavaScript includes. No URL configuration. Just render the form.

## How It Works

- JavaScript is automatically embedded when the first chained field renders
- For static `choices_map`, the choice tree is embedded as JSON (no server calls)
- For database `choices_callback`, AJAX calls go to an auto-registered endpoint
- The mixin detects `parent_field` relationships and wires everything together

## Database-Backed Choices (Also No URL Config!)

For choices stored in your database, just use a `choices_callback`. The AJAX endpoint is auto-registered.

### Self-Referential Model (Recommended)

A single model with a `parent` field is the cleanest approach for hierarchies:

```python
# models.py
class MageFaction(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='children'
    )

# forms.py  
def get_children(parent_id):
    if not parent_id:
        return []
    return list(MageFaction.objects.filter(
        parent_id=parent_id
    ).values_list('id', 'name'))

class MageFactionForm(ChainedSelectMixin, forms.Form):
    # No chained_ajax_url needed!
    
    affiliation = forms.ModelChoiceField(
        queryset=MageFaction.objects.filter(parent__isnull=True),
        empty_label="Select affiliation..."
    )
    
    faction = ChainedChoiceField(
        parent_field='affiliation',
        choices_callback=get_children,
        empty_label="Select faction..."
    )
    
    subfaction = ChainedChoiceField(
        parent_field='faction',
        choices_callback=get_children,  # Same function!
        empty_label="Select subfaction...",
        required=False,
    )
```

**No urls.py changes needed!** The app auto-registers `/__chained_select__/` which dynamically imports your form class and calls the appropriate `choices_callback`.

### Separate Models (Country/State/City)

The same pattern works with separate models - just define a `choices_callback` for each level:

```python
def get_states(country_id):
    return list(State.objects.filter(country_id=country_id).values_list('id', 'name'))

def get_cities(state_id):
    return list(City.objects.filter(state_id=state_id).values_list('id', 'name'))

class LocationForm(ChainedSelectMixin, forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    state = ChainedChoiceField(parent_field='country', choices_callback=get_states)
    city = ChainedChoiceField(parent_field='state', choices_callback=get_cities)
```

### Custom AJAX URL (Optional)

If you prefer to use your own endpoint instead of the auto-registered one:

```python
class MyForm(ChainedSelectMixin, forms.Form):
    chained_ajax_url = '/my/custom/endpoint/'
    # ...
```

## API Reference

### ChainedChoiceField

```python
ChainedChoiceField(
    choices=[],           # For root fields: static choices
    parent_field=None,    # Name of the parent field this depends on
    choices_map=None,     # Dict: parent_value -> [(value, label), ...]
    choices_callback=None,# Function: parent_value -> [(value, label), ...]
    empty_label="---",    # Label for the empty option
)
```

### ChainedSelectMixin

Add to your form class. Automatically detects and configures chained fields.

```python
class MyForm(ChainedSelectMixin, forms.Form):
    chained_ajax_url = None  # Optional: override auto-registered URL
    # ... fields ...
```

### make_ajax_view

Factory for creating AJAX endpoints:

```python
from chained_select import make_ajax_view

view = make_ajax_view({
    'field_name': callable_or_config,
    # ...
})
```

## Features

- **Truly zero config** - Just render `{{ form.as_p }}`, nothing else needed
- **Self-contained** - JavaScript auto-injects on first field render
- **Auto AJAX endpoint** - `/__chained_select__/` registered via AppConfig
- **Validation included** - Ensures child selections are valid for parent
- **Initial data support** - Pre-populates choices when editing existing data
- **Formset compatible** - Handles Django's form prefixes
- **Framework integration** - Auto-reinits for htmx and Hotwire Turbo

## Examples

See the `examples/` directory:
- `mage_model.py` - **Recommended**: Self-referential `MageFaction` model with parent field
- `mage_simple.py` - Static choices using `choices_map` (no database)
- `database_backed.py` - Generic pattern for separate models per level

## License

MIT
