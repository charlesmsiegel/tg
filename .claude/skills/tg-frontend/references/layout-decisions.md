# Layout Decisions

Guidelines for choosing between layout patterns and applying consistent styling details.

## Border Radius Standards

| Element Type | Radius | Examples |
|-------------|--------|----------|
| Small elements | `4px` to `6px` | Badges, inline stat boxes |
| Medium elements | `6px` to `8px` | Content boxes, cards |

**Rule:** Never use sharp corners—always apply border-radius.

## Link Styling

### Text Links
- Use standard link styling (no badges or buttons)
- For hierarchy, use arrows: `Parent → Child`
- Example: Faction displays should be plain text links

### Card Links
- Links within cards: `font-weight: 500` to `600`
- Maintain proper contrast for accessibility

## Compact vs Spacious Layouts

### Use Compact When:
- Multiple related fields in one card
- Information needs quick scanning
- Secondary/supporting information
- Padding: `16px` to `20px`

### Use Spacious When:
- Primary statistics or key information
- Single important values
- Emphasizing importance
- Padding: `24px` to `32px`

## Table vs Card vs Stat Box

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Tables** | Tabular data with many rows | Scene lists, XP logs |
| **Card grids** | Items with multiple properties | Resonance, merits/flaws, characters |
| **Stat boxes** | Key statistics (1-6 values) | Population, barriers, energy output |

**Preference order:** Stat boxes → Card grids → Tables

## Responsive Breakpoints

| Size | Class Prefix | Min Width |
|------|--------------|-----------|
| Small | `col-sm-*` | ≥576px |
| Medium | `col-md-*` | ≥768px |
| Large | `col-lg-*` | ≥992px |
| Extra Large | `col-xl-*` | ≥1200px |

### Mobile Patterns
- Stack columns on mobile: `col-12 col-md-6`
- Margin on mobile only: `mb-3 mb-md-0`
- Touch targets: minimum 44px
- Test centering on mobile
