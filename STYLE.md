# UI Design Style Guide

This document outlines the design principles and patterns used throughout the application to ensure consistency and maintainability.

## Core Design Principles

### 1. Centered Layouts
- **Card headers** should be centered using `text-center` class
- **Main content** should be centered when appropriate for better visual balance
- **Large stat displays** (population, ratings, etc.) should be centered prominently

### 2. Consistent Component Usage

#### Cards
- Use `tg-card` instead of `card`
- Use `tg-card-header` instead of `card-header`
- Use `tg-card-body` instead of `card-body`
- Use `tg-card-title` instead of `card-title`
- Use `tg-card-subtitle` instead of `card-subtitle`

#### Badges
- Use `tg-badge` instead of `badge`
- Add `badge-pill` for rounded badges (e.g., status indicators)
- Avoid overusing badges - prefer clean text or stat boxes for most content

#### Tables
- Use `tg-table` instead of `table`
- Center table content with `text-align: center;` on headers and cells
- Add proper spacing: `padding: 12px 16px;` for headers, `padding: 14px 16px;` for cells

### 3. Spacing Standards

#### Card Padding
- Standard card body padding: `20px` to `24px`
- Compact layouts: `20px`
- Spacious layouts: `24px` to `32px`

#### Margins
- Between major sections: `mb-4` or `mb-5`
- Between related items: `mb-3`
- Between closely related items: `mb-2`
- Inline spacing: `8px` between label and value

### 4. Typography

#### Headers
- Card titles: Use `tg-card-title` with appropriate gameline class (`mta_heading`, `wta_heading`, etc.)
- Section headers within cards: Use `<h6>` with gameline class
- Subsection labels: Use uppercase with `font-size: 0.75rem`, `letter-spacing: 0.5px`, `font-weight: 600`

#### Body Text
- Standard text: Default font size with `line-height: 1.6` for readability
- Labels: `font-weight: 600`, `color: var(--theme-text-secondary)`
- Values: `font-weight: 700`, `color: var(--theme-text-primary)`

#### Stat Displays
- Large numbers: `font-size: 1.5rem` to `1.75rem`, `font-weight: 700`
- Medium numbers: `font-size: 1.25rem`, `font-weight: 700`
- Small inline values: `font-size: 0.9rem` to `1rem`

### 5. Stat Box Pattern

For displaying key statistics (population, ratings, barriers, etc.):

```html
<div style="display: inline-block; padding: 12px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Label:</span>
    <span style="font-weight: 700; color: var(--theme-text-primary);">Value</span>
</div>
```

For larger stat displays with label above value:

```html
<div style="padding: 16px; border-radius: 8px; background-color: rgba(0,0,0,0.05);">
    <h6 class="mb-2" style="font-weight: 600; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary);">Label</h6>
    <div style="font-size: 1.75rem; font-weight: 700; color: var(--theme-text-primary);">Value</div>
</div>
```

### 6. Content Box Pattern

For displaying text content (descriptions, constraints, etc.):

```html
<div style="padding: 12px 16px; border-radius: 6px; background-color: rgba(0,0,0,0.02); text-align: center;">
    <p class="mb-0" style="line-height: 1.6;">Content text here</p>
</div>
```

### 7. Grid Layouts

#### Two-Column Layouts
```html
<div class="row">
    <div class="col-md-6 mb-3">
        <!-- Left column content -->
    </div>
    <div class="col-md-6 mb-3">
        <!-- Right column content -->
    </div>
</div>
```

#### Three-Column Layouts (for stats)
```html
<div class="row text-center">
    <div class="col-md-4 mb-3 mb-md-0">
        <!-- Stat 1 -->
    </div>
    <div class="col-md-4 mb-3 mb-md-0">
        <!-- Stat 2 -->
    </div>
    <div class="col-md-4 mb-3 mb-md-0">
        <!-- Stat 3 -->
    </div>
</div>
```

#### Responsive Card Grids
```html
<div class="row">
    {% for item in items %}
        <div class="col-sm-6 col-md-4 mb-3">
            <div class="tg-card h-100">
                <!-- Card content -->
            </div>
        </div>
    {% endfor %}
</div>
```

### 8. Color Usage

#### Backgrounds
- Primary stat boxes: `rgba(0,0,0,0.05)`
- Secondary content boxes: `rgba(0,0,0,0.02)`
- Hover states: Slightly darker than base

#### Text Colors
- Primary text: `var(--theme-text-primary)`
- Secondary text (labels): `var(--theme-text-secondary)`
- Muted text: `text-muted` class

#### Status Colors
- Success/Positive: Green (`#28a745` with `rgba(40, 167, 69, 0.1)` background)
- Warning: Yellow/Orange
- Danger/Negative: Red (`#dc3545` with `rgba(220, 53, 69, 0.1)` background)
- Info: Blue

#### Status Badges
Use standardized badge classes for character, location, and item statuses:
- **Unfinished** (`badge-un`): Gray/Neutral - `rgba(108, 117, 125, 0.15)` background, `#6c757d` text
- **Submitted** (`badge-sub`): Blue/Info - `rgba(23, 162, 184, 0.15)` background, `#17a2b8` text
- **Approved** (`badge-app`): Green/Success - `rgba(40, 167, 69, 0.15)` background, `#28a745` text
- **Retired** (`badge-ret`): Orange/Warning - `rgba(255, 193, 7, 0.15)` background, `#d39e00` text
- **Deceased** (`badge-dec`): Red/Danger - `rgba(220, 53, 69, 0.15)` background, `#dc3545` text

Usage: `<span class="tg-badge badge-{{ object.status|lower }}">{{ object.get_status_display }}</span>`

### 9. Border Radius Standards
- Small elements (badges, inline boxes): `4px` to `6px`
- Medium elements (content boxes, cards): `6px` to `8px`
- Never use sharp corners - always apply border-radius

### 10. Gameline-Specific Styling

#### Data Attributes
Add `data-gameline` attribute to header cards:
- Mage: `data-gameline="mta"`
- Werewolf: `data-gameline="wta"`
- Vampire: `data-gameline="vta"`
- etc.

#### Heading Classes
Apply gameline-specific classes to headers:
- Mage: `mta_heading`
- Werewolf: `wta_heading`
- Vampire: `vta_heading`
- etc.

### 11. Link Styling

#### Text Links
- Use standard link styling (no badges or buttons)
- Example: Faction displays should be plain text links with arrows (→) for hierarchy

#### Card Links
- Links within cards should have `font-weight: 500` to `600`
- Maintain proper contrast for accessibility

### 12. Compact vs. Spacious Layouts

#### When to Use Compact
- Multiple related fields in one card
- Information that needs to be scannable quickly
- Secondary information

#### When to Use Spacious
- Primary statistics or key information
- Single important values
- When emphasizing importance

### 13. Responsive Design

#### Mobile Considerations
- Use `mb-3 mb-md-0` to add bottom margin on mobile but remove on desktop
- Stack columns on mobile: `col-12 col-md-6`
- Ensure touch targets are at least 44px
- Test centering on mobile devices

#### Breakpoints
- Small: `col-sm-*` (≥576px)
- Medium: `col-md-*` (≥768px)
- Large: `col-lg-*` (≥992px)
- Extra Large: `col-xl-*` (≥1200px)

### 14. Table Alternatives

Prefer card-based layouts over tables when possible:
- **Tables**: Use for tabular data with many rows (scenes list, etc.)
- **Card grids**: Use for items with multiple properties (resonance, merits/flaws, characters)
- **Stat boxes**: Use for key statistics (population, barriers, energy output)

### 15. Consistency Checklist

When creating or updating a template, ensure:
- [ ] All cards use `tg-card` components
- [ ] Headers are centered where appropriate
- [ ] Spacing follows the standards (20-24px padding, proper margins)
- [ ] Typography uses consistent sizes and weights
- [ ] Gameline classes are applied correctly
- [ ] Layout is responsive (mobile-friendly)
- [ ] Colors use CSS variables or standard patterns
- [ ] Border radius is applied consistently
- [ ] Content is scannable and well-organized

## Examples

### Good: Modern Stat Display
```html
<div class="tg-card">
    <div class="tg-card-header text-center">
        <h5 class="tg-card-title mta_heading">Node Properties</h5>
    </div>
    <div class="tg-card-body text-center" style="padding: 20px;">
        <div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
            <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Size:</span>
            <span style="font-weight: 700; color: var(--theme-text-primary);">{{ value }}</span>
        </div>
    </div>
</div>
```

### Bad: Old Table-Heavy Layout
```html
<div class="card">
    <div class="card-header">
        <h5>Properties</h5>
    </div>
    <div class="card-body">
        <table class="table">
            <tr>
                <td>Size</td>
                <td>{{ value }}</td>
            </tr>
        </table>
    </div>
</div>
```

## Maintenance

This style guide should be updated as new patterns emerge or existing patterns are refined. When making changes:
1. Update this document first
2. Apply changes consistently across all templates
3. Test on multiple screen sizes
4. Verify accessibility (contrast, touch targets, etc.)
