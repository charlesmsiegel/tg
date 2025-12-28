---
name: tg-frontend
description: Frontend design system for Tellurium Games World of Darkness web application. Use when creating/modifying HTML templates (detail views, forms, lists), implementing components or stat displays, reviewing templates for design consistency, applying gameline-specific theming (Mage, Vampire, Werewolf, Changeling, Wraith, Hunter, Demon, Mummy), building responsive layouts, or styling forms. Triggers on WoD template work, tg-card components, gameline headings, Django template tags like dots/boxes filters.
---

# TG Frontend Design System

## Quick Reference

### Always Use TG Components

| Use | NOT |
|-----|-----|
| `tg-card` | `card` |
| `tg-card-header` | `card-header` |
| `tg-card-body` | `card-body` |
| `tg-btn` | `btn` |
| `tg-badge` | `badge` |
| `tg-table` | `table` |

### Gameline Classes

| Gameline | Heading | Badge | Data Attr |
|----------|---------|-------|-----------|
| Mage | `mta_heading` | `badge-mta` | `data-gameline="mta"` |
| Vampire | `vtm_heading` | `badge-vtm` | `data-gameline="vtm"` |
| Werewolf | `wta_heading` | `badge-wta` | `data-gameline="wta"` |
| Changeling | `ctd_heading` | `badge-ctd` | `data-gameline="ctd"` |
| Wraith | `wto_heading` | `badge-wto` | `data-gameline="wto"` |
| Hunter | `htr_heading` | `badge-htr` | `data-gameline="htr"` |
| Demon | `dtf_heading` | `badge-dtf` | `data-gameline="dtf"` |
| Mummy | `mtr_heading` | `badge-mtr` | `data-gameline="mtr"` |

Use `{{ object.get_heading }}` and `{{ object.get_badge_class }}` for dynamic classes.

### Template Tags

```html
{% load sanitize_text dots %}
{{ rating|dots }}       {# ●●●○○ #}
{{ rating|dots:10 }}    {# explicit max 10 #}
{{ value|boxes }}       {# ■■■□□ for temp values #}
{{ content|sanitize_html|linebreaks }}
```

### Status Badges

```html
<span class="tg-badge badge-{{ object.status|lower }}">{{ object.get_status_display }}</span>
```

`badge-un` (gray), `badge-sub` (blue), `badge-app` (green), `badge-ret` (orange), `badge-dec` (red)

## Task-Based Workflow

### Creating/Editing Detail Views

1. Read [references/detail-patterns.md](references/detail-patterns.md) for component patterns
2. Read [references/detail-examples.md](references/detail-examples.md) for real working examples
3. Extend appropriate base: `core/object.html`, `locations/core/location/detail.html`, `characters/core/character/detail.html`, `items/core/item/detail.html`

### Creating/Editing Forms

1. Read [references/form-patterns.md](references/form-patterns.md) for field patterns
2. Read [references/form-examples.md](references/form-examples.md) for the Haven gold standard
3. Extend `core/form.html`

### Choosing Layout Patterns

Read [references/layout-decisions.md](references/layout-decisions.md) for guidance on:
- Border radius standards (4-6px vs 6-8px)
- Link styling (text links vs card links)
- Compact vs spacious layouts
- When to use tables vs card grids vs stat boxes
- Responsive breakpoints

## Quick Patterns (No Reference Needed)

**Page Header Card:**
```html
<div class="tg-card header-card mb-4" data-gameline="mta">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
    </div>
</div>
```

**Section Card:**
```html
<div class="tg-card">
    <div class="tg-card-header text-center">
        <h5 class="tg-card-title {{ object.get_heading }}">Section Title</h5>
    </div>
    <div class="tg-card-body text-center" style="padding: 20px;">
        <!-- Content -->
    </div>
</div>
```

**Form Field:**
```html
<div class="row mb-3">
    <div class="col-md-6">
        <label for="{{ form.name.id_for_label }}" class="form-label">Name</label>
        {{ form.name }}
    </div>
</div>
```

**Checkbox:**
```html
<div class="form-check">
    {{ form.field }}
    <label class="form-check-label" for="{{ form.field.id_for_label }}">Label</label>
</div>
```

## Core Style Rules

### Typography
- Labels: `font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary);`
- Values: `font-weight: 700; color: var(--theme-text-primary);`
- Large numbers: `font-size: 1.5rem; font-weight: 700;`

### Spacing
- Card body: `padding: 20px;` (standard) or `padding: 24px;` (spacious)
- Section gaps: `mb-4` or `mb-5`
- Related items: `mb-3`
- Label-value gap: `margin-right: 8px`

### Backgrounds
- Primary stat: `rgba(0,0,0,0.05)`
- Content box: `rgba(0,0,0,0.02)`
- Active feature: `rgba(0,255,0,0.1)`

### Responsive Columns
- Two-column: `col-md-6`
- Three-column: `col-md-4`
- Card grid: `col-sm-6 col-md-4 col-lg-3`
- Equal height: add `h-100` to cards
- Mobile margin: `mb-3 mb-md-0`

## Consistency Checklist

- [ ] All cards use `tg-card` (not Bootstrap `card`)
- [ ] Headers have gameline class and `data-gameline`
- [ ] Headers centered where appropriate
- [ ] Labels uppercase, values bold
- [ ] Forms use `form-label` class
- [ ] Checkboxes in `form-check` divs
- [ ] Template loads `{% load dots sanitize_text %}`
- [ ] Equal-height cards use `h-100`
- [ ] Responsive with proper column classes

## Reference Files in Codebase

- Style guide: `SOURCES/STYLE.md`
- CSS components: `static/themes/components.css`
- Base styles: `static/style.css`
