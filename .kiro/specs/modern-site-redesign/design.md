# Design Document

## Overview

This design document outlines the approach for redesigning the Tellurium Games World of Darkness site with a modern, consistent visual design system. The redesign will leverage the existing component library and theme system while updating all templates across the Django apps to provide a cohesive, attractive user experience.

### Design Goals

1. **Visual Consistency**: Establish uniform design patterns across all apps using the existing TG component library
2. **Modern Aesthetics**: Implement contemporary design trends including card-based layouts, generous whitespace, and smooth interactions
3. **Theme Compatibility**: Ensure all design elements work seamlessly in both light and dark modes
4. **Gameline Identity**: Consistently apply gameline-specific fonts to reinforce visual identity
5. **Minimal File Creation**: Reuse and enhance existing CSS and template files rather than creating new ones
6. **Accessibility**: Meet WCAG 2.1 AA standards for contrast, keyboard navigation, and screen reader support

### Design Principles

- **Component-First**: Use TG-prefixed components (tg-card, tg-btn, tg-badge) as building blocks
- **Progressive Enhancement**: Start with semantic HTML, enhance with CSS, add JavaScript only when necessary
- **Mobile-First**: Design for mobile viewports first, then enhance for larger screens
- **Content-Focused**: Let content breathe with appropriate spacing and hierarchy
- **Performance-Conscious**: Minimize CSS specificity, avoid unnecessary animations, optimize font loading

## Architecture

### Design System Structure

```
static/themes/
├── master-theme.css          # Main entry point (existing, no changes)
├── theme-system.css          # CSS custom properties (enhance existing)
├── theme-application.css     # Apply properties to elements (enhance existing)
├── components.css            # Base components (enhance existing)
├── character-components.css  # Character-specific components (enhance existing)
├── fonts.css                 # Font definitions (existing, no changes)
├── health-system.css         # Health tracking (existing, no changes)
└── highlight.css             # Text highlighting (existing, no changes)
```

### Template Structure

All templates follow a consistent hierarchy:

```
base.html (core/templates/core/base.html)
├── Navigation (navbar)
├── Content Block
│   ├── Page Header (tg-card with gameline-specific heading)
│   ├── Main Content (tg-card sections)
│   └── Action Area (forms, buttons)
└── Footer (messages, scripts)
```

### Component Hierarchy

1. **Layout Components**: Container, row, column (Bootstrap grid)
2. **Card Components**: tg-card, tg-card-header, tg-card-body, tg-card-footer
3. **Button Components**: tg-btn with variants (primary, secondary, outline, etc.)
4. **Badge Components**: tg-badge with variants (gameline, status, info)
5. **Form Components**: tg-form-group, tg-form-control, tg-form-feedback
6. **Navigation Components**: Tabs, breadcrumbs, pagination
7. **Data Display**: Tables, lists, definition lists

## Components and Interfaces

### Enhanced Color Palette

The existing theme system will be enhanced with additional semantic colors:

```css
/* Enhanced Theme Colors (additions to theme-system.css) */
:root {
  /* Accent Colors */
  --color-accent-1: #3498db;  /* Blue accent */
  --color-accent-2: #9b59b6;  /* Purple accent */
  --color-accent-3: #e67e22;  /* Orange accent */
  
  /* Status Colors (enhanced) */
  --color-status-active: #28a745;
  --color-status-inactive: #6c757d;
  --color-status-pending: #ffc107;
  --color-status-deceased: #dc3545;
  --color-status-npc: #17a2b8;
  
  /* Gameline Accent Colors (lighter variants for backgrounds) */
  --gameline-vtm-light: rgba(139, 0, 0, 0.1);
  --gameline-wta-light: rgba(34, 139, 34, 0.1);
  --gameline-mta-light: rgba(75, 0, 130, 0.1);
  --gameline-ctd-light: rgba(255, 105, 180, 0.1);
  --gameline-wto-light: rgba(47, 79, 79, 0.1);
  
  /* Interactive States */
  --color-hover-overlay: rgba(0, 0, 0, 0.05);
  --color-active-overlay: rgba(0, 0, 0, 0.1);
  --color-focus-ring: rgba(30, 126, 52, 0.25);
}

/* Dark Theme Adjustments */
@media (prefers-color-scheme: dark) {
  :root:not(.theme-light) {
    --color-hover-overlay: rgba(255, 255, 255, 0.05);
    --color-active-overlay: rgba(255, 255, 255, 0.1);
  }
}
```

### Page Header Component

A standardized page header component for all index and detail pages:

```html
<!-- Page Header Pattern -->
<div class="tg-card header-card mb-4">
  <div class="tg-card-header">
    <h1 class="tg-card-title [gameline]_heading">
      {{ page_title }}
    </h1>
    <div class="tg-card-actions">
      <!-- Action buttons -->
    </div>
  </div>
</div>
```

CSS for page headers (add to components.css):

```css
/* Page Header Styling */
.header-card .tg-card-header {
  min-height: 4rem;
  background: linear-gradient(135deg, var(--theme-card-header-bg) 0%, var(--theme-bg-secondary) 100%);
}

.header-card .tg-card-title {
  font-size: var(--font-size-3xl);
  font-weight: 600;
  margin: 0;
}

/* Gameline-specific header styling */
.header-card[data-gameline="vtm"] .tg-card-title {
  font-family: var(--font-family-vtm);
  color: var(--gameline-vtm);
}

.header-card[data-gameline="wta"] .tg-card-title {
  font-family: var(--font-family-wta);
  color: var(--gameline-wta);
}

.header-card[data-gameline="mta"] .tg-card-title {
  font-family: var(--font-family-mta);
  color: var(--gameline-mta);
}

.header-card[data-gameline="ctd"] .tg-card-title {
  font-family: var(--font-family-ctd);
  color: var(--gameline-ctd);
}

.header-card[data-gameline="wto"] .tg-card-title {
  font-family: var(--font-family-wto);
  color: var(--gameline-wto);
}

@media (max-width: 768px) {
  .header-card .tg-card-title {
    font-size: var(--font-size-2xl);
  }
}
```

### List/Index Page Pattern

Standardized layout for all index pages (characters, locations, items):

```html
<div class="container py-4">
  <!-- Page Header -->
  <div class="tg-card header-card mb-4" data-gameline="{{ gameline }}">
    <div class="tg-card-header">
      <h1 class="tg-card-title {{ gameline }}_heading">{{ title }}</h1>
    </div>
  </div>

  <!-- Tabbed Content -->
  <div class="tg-card mb-4">
    <div class="tg-card-header">
      <!-- Navigation tabs -->
    </div>
    <div class="tg-card-body">
      <!-- List content -->
    </div>
  </div>

  <!-- Action Area (if applicable) -->
  <div class="tg-card">
    <div class="tg-card-header">
      <h5 class="tg-card-title">{{ action_title }}</h5>
    </div>
    <div class="tg-card-body">
      <!-- Forms or actions -->
    </div>
  </div>
</div>
```

### Detail Page Pattern

Standardized layout for all detail pages:

```html
<div class="container py-4">
  <!-- Object Header -->
  <div class="tg-card header-card mb-4" data-gameline="{{ object.gameline }}">
    <div class="tg-card-header">
      <div>
        <h1 class="tg-card-title {{ object.gameline }}_heading">{{ object.name }}</h1>
        <p class="tg-card-subtitle">{{ object.type }} | {{ object.chronicle }}</p>
      </div>
      <div class="tg-card-actions">
        <a href="{{ edit_url }}" class="tg-btn btn-primary btn-sm">
          <i class="fas fa-edit"></i> Edit
        </a>
      </div>
    </div>
  </div>

  <!-- Content Sections -->
  <div class="row">
    <div class="col-lg-8">
      <!-- Main content sections -->
      <div class="tg-card mb-4">
        <div class="tg-card-header">
          <h3 class="tg-card-title">Section Title</h3>
        </div>
        <div class="tg-card-body">
          <!-- Section content -->
        </div>
      </div>
    </div>
    
    <div class="col-lg-4">
      <!-- Sidebar content -->
      <div class="tg-card mb-4">
        <div class="tg-card-header">
          <h4 class="tg-card-title">Quick Info</h4>
        </div>
        <div class="tg-card-body">
          <!-- Sidebar content -->
        </div>
      </div>
    </div>
  </div>
</div>
```

### Enhanced Table Styling

Improved table component for data display (add to components.css):

```css
/* Enhanced Table Component */
.tg-table {
  width: 100%;
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
}

.tg-table thead th {
  background-color: var(--theme-bg-secondary);
  color: var(--theme-text-primary);
  font-weight: 600;
  text-transform: uppercase;
  font-size: var(--font-size-xs);
  letter-spacing: 0.5px;
  padding: var(--spacing-3) var(--spacing-4);
  border-bottom: 2px solid var(--theme-border-color);
  text-align: left;
}

.tg-table tbody td {
  padding: var(--spacing-3) var(--spacing-4);
  border-bottom: 1px solid var(--theme-border-light);
  vertical-align: middle;
  color: var(--theme-text-primary);
}

.tg-table tbody tr {
  transition: var(--transition-fast);
}

.tg-table tbody tr:hover {
  background-color: var(--color-hover-overlay);
}

.tg-table tbody tr:last-child td {
  border-bottom: none;
}

/* Striped variant */
.tg-table.table-striped tbody tr:nth-of-type(odd) {
  background-color: var(--theme-bg-tertiary);
}

/* Compact variant */
.tg-table.table-compact thead th,
.tg-table.table-compact tbody td {
  padding: var(--spacing-2) var(--spacing-3);
}

/* Responsive table wrapper */
.tg-table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media (max-width: 768px) {
  .tg-table thead {
    display: none;
  }
  
  .tg-table tbody tr {
    display: block;
    margin-bottom: var(--spacing-4);
    border: 1px solid var(--theme-border-color);
    border-radius: var(--border-radius-base);
  }
  
  .tg-table tbody td {
    display: flex;
    justify-content: space-between;
    padding: var(--spacing-2) var(--spacing-3);
    border-bottom: 1px solid var(--theme-border-light);
  }
  
  .tg-table tbody td:before {
    content: attr(data-label);
    font-weight: 600;
    text-transform: uppercase;
    font-size: var(--font-size-xs);
    color: var(--theme-text-secondary);
  }
  
  .tg-table tbody td:last-child {
    border-bottom: none;
  }
}
```

### Form Styling Enhancements

Enhanced form components (add to components.css):

```css
/* Enhanced Form Components */
.tg-form-group {
  margin-bottom: var(--spacing-4);
}

.tg-form-label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-weight: 500;
  color: var(--theme-text-primary);
  font-size: var(--font-size-sm);
}

.tg-form-label.required::after {
  content: ' *';
  color: var(--color-danger);
}

.tg-form-control {
  display: block;
  width: 100%;
  padding: var(--spacing-2) var(--spacing-3);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  color: var(--theme-text-primary);
  background-color: var(--theme-input-bg);
  border: 1px solid var(--theme-input-border);
  border-radius: var(--border-radius-base);
  transition: var(--transition-fast);
}

.tg-form-control:focus {
  outline: 0;
  border-color: var(--theme-input-focus-border);
  box-shadow: 0 0 0 0.2rem var(--color-focus-ring);
}

.tg-form-control::placeholder {
  color: var(--theme-text-muted);
  opacity: 1;
}

.tg-form-control:disabled {
  background-color: var(--theme-bg-tertiary);
  opacity: 0.6;
  cursor: not-allowed;
}

/* Form control sizes */
.tg-form-control.form-control-sm {
  padding: var(--spacing-1) var(--spacing-2);
  font-size: var(--font-size-sm);
}

.tg-form-control.form-control-lg {
  padding: var(--spacing-3) var(--spacing-4);
  font-size: var(--font-size-lg);
}

/* Select styling */
.tg-form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%23333' d='M6 9L1 4h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--spacing-3) center;
  background-size: 12px;
  padding-right: var(--spacing-8);
}

/* Checkbox and radio styling */
.tg-form-check {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-2);
}

.tg-form-check-input {
  width: 1.25rem;
  height: 1.25rem;
  margin-right: var(--spacing-2);
  cursor: pointer;
}

.tg-form-check-label {
  margin-bottom: 0;
  cursor: pointer;
  user-select: none;
}

/* Form validation states */
.tg-form-control.is-valid {
  border-color: var(--color-success);
}

.tg-form-control.is-valid:focus {
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

.tg-form-control.is-invalid {
  border-color: var(--color-danger);
}

.tg-form-control.is-invalid:focus {
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

.tg-form-feedback {
  margin-top: var(--spacing-1);
  font-size: var(--font-size-sm);
}

.tg-form-feedback.valid-feedback {
  color: var(--color-success);
}

.tg-form-feedback.invalid-feedback {
  color: var(--color-danger);
}

.tg-form-help {
  margin-top: var(--spacing-1);
  font-size: var(--font-size-sm);
  color: var(--theme-text-muted);
}

/* Inline forms */
.tg-form-inline {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--spacing-3);
}

.tg-form-inline .tg-form-group {
  margin-bottom: 0;
}

@media (max-width: 576px) {
  .tg-form-inline {
    flex-direction: column;
    align-items: stretch;
  }
  
  .tg-form-inline .tg-form-group {
    width: 100%;
  }
}
```

### Navigation Tab Styling

Enhanced tab navigation (add to components.css):

```css
/* Enhanced Tab Navigation */
.tg-nav-tabs {
  display: flex;
  flex-wrap: wrap;
  border-bottom: 2px solid var(--theme-border-color);
  margin-bottom: var(--spacing-4);
  gap: var(--spacing-1);
}

.tg-nav-tabs .tg-nav-link {
  display: block;
  padding: var(--spacing-2) var(--spacing-4);
  color: var(--theme-text-secondary);
  text-decoration: none;
  border: 1px solid transparent;
  border-bottom: none;
  border-top-left-radius: var(--border-radius-base);
  border-top-right-radius: var(--border-radius-base);
  transition: var(--transition-fast);
  font-weight: 500;
  position: relative;
  bottom: -2px;
}

.tg-nav-tabs .tg-nav-link:hover {
  color: var(--theme-text-primary);
  background-color: var(--color-hover-overlay);
}

.tg-nav-tabs .tg-nav-link.active {
  color: var(--color-primary);
  background-color: var(--theme-bg-primary);
  border-color: var(--theme-border-color) var(--theme-border-color) var(--theme-bg-primary);
  border-bottom: 2px solid var(--color-primary);
}

.tg-nav-tabs .tg-nav-link:focus {
  outline: 0;
  box-shadow: 0 0 0 0.2rem var(--color-focus-ring);
}

/* Pill variant */
.tg-nav-pills {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-2);
  margin-bottom: var(--spacing-4);
}

.tg-nav-pills .tg-nav-link {
  display: block;
  padding: var(--spacing-2) var(--spacing-4);
  color: var(--theme-text-secondary);
  text-decoration: none;
  border-radius: var(--border-radius-full);
  transition: var(--transition-fast);
  font-weight: 500;
}

.tg-nav-pills .tg-nav-link:hover {
  color: var(--theme-text-primary);
  background-color: var(--color-hover-overlay);
}

.tg-nav-pills .tg-nav-link.active {
  color: var(--color-white);
  background-color: var(--color-primary);
}

@media (max-width: 576px) {
  .tg-nav-tabs,
  .tg-nav-pills {
    flex-direction: column;
  }
  
  .tg-nav-tabs .tg-nav-link {
    border-radius: var(--border-radius-base);
    border-bottom: 1px solid transparent;
    bottom: 0;
  }
  
  .tg-nav-tabs .tg-nav-link.active {
    border-left: 3px solid var(--color-primary);
    border-bottom: 1px solid var(--theme-border-color);
  }
}
```

## Data Models

No changes to Django models are required. The redesign is purely presentational and works with existing data structures.

### Template Context Requirements

Templates will expect the following context variables (already provided by existing views):

- `object` or specific model instance (character, location, item, etc.)
- `title` - Page title
- `header` - CSS class for gameline-specific styling (e.g., "vtm_heading")
- `user` - Current user for permissions
- `chronicles` - List of chronicles for navigation
- Form objects for create/edit pages

## Error Handling

### Graceful Degradation

1. **Font Loading**: If gameline fonts fail to load, fallback to system serif fonts
2. **CSS Custom Properties**: Provide fallback values for older browsers
3. **JavaScript**: All functionality works without JavaScript (progressive enhancement)
4. **Images**: Provide alt text and fallback backgrounds

### Error States

Visual feedback for common error scenarios:

```css
/* Error State Styling */
.tg-error-message {
  padding: var(--spacing-4);
  background-color: rgba(220, 53, 69, 0.1);
  border-left: 4px solid var(--color-danger);
  border-radius: var(--border-radius-base);
  color: var(--color-danger);
  margin-bottom: var(--spacing-4);
}

.tg-warning-message {
  padding: var(--spacing-4);
  background-color: rgba(255, 193, 7, 0.1);
  border-left: 4px solid var(--color-warning);
  border-radius: var(--border-radius-base);
  color: var(--color-warning);
  margin-bottom: var(--spacing-4);
}

.tg-info-message {
  padding: var(--spacing-4);
  background-color: rgba(23, 162, 184, 0.1);
  border-left: 4px solid var(--color-info);
  border-radius: var(--border-radius-base);
  color: var(--color-info);
  margin-bottom: var(--spacing-4);
}

.tg-success-message {
  padding: var(--spacing-4);
  background-color: rgba(40, 167, 69, 0.1);
  border-left: 4px solid var(--color-success);
  border-radius: var(--border-radius-base);
  color: var(--color-success);
  margin-bottom: var(--spacing-4);
}
```

## Testing Strategy

### Visual Regression Testing

1. **Manual Testing**: Test each template in both light and dark themes
2. **Browser Testing**: Test in Chrome, Firefox, Safari, Edge
3. **Device Testing**: Test on mobile (iOS/Android), tablet, desktop
4. **Gameline Testing**: Verify font application for each gameline

### Accessibility Testing

1. **Keyboard Navigation**: Tab through all interactive elements
2. **Screen Reader**: Test with NVDA/JAWS/VoiceOver
3. **Contrast**: Verify WCAG AA contrast ratios using browser tools
4. **Focus Indicators**: Ensure visible focus states on all interactive elements

### Functional Testing

1. **Form Submission**: Verify all forms work correctly
2. **Navigation**: Test all links and navigation elements
3. **Responsive Behavior**: Test layout at various breakpoints
4. **Theme Switching**: Verify theme toggle works correctly

### Test Checklist by App

**Characters App**:
- [ ] Character index page displays correctly with tabs
- [ ] Character detail page shows all sections properly
- [ ] Character creation form works
- [ ] Gameline fonts apply to character names
- [ ] Status badges display correctly

**Locations App**:
- [ ] Location index page displays correctly
- [ ] Location detail page shows all attributes
- [ ] Location forms work properly
- [ ] Gameline fonts apply to location names

**Items App**:
- [ ] Item index page displays correctly
- [ ] Item detail page shows all properties
- [ ] Item forms work properly
- [ ] Gameline fonts apply to item names

**Game App**:
- [ ] Chronicle pages display correctly
- [ ] Scene pages display correctly
- [ ] Game-related forms work properly

**Accounts App**:
- [ ] Profile pages display correctly
- [ ] Login/signup forms work properly
- [ ] Theme selection works

**Core App**:
- [ ] Home page displays correctly
- [ ] Navigation works across all pages
- [ ] House rules pages display correctly

## Implementation Approach

### Phase 1: CSS Enhancements

1. Add new color variables to `theme-system.css`
2. Add enhanced component styles to `components.css`
3. Add page header styles to `components.css`
4. Add table enhancements to `components.css`
5. Add form enhancements to `components.css`
6. Add navigation enhancements to `components.css`

### Phase 2: Core Templates

1. Update `core/templates/core/base.html` (if needed for consistency)
2. Update `core/templates/core/index.html`
3. Update `core/templates/core/form.html`

### Phase 3: Characters App Templates

1. Update `characters/templates/characters/index.html`
2. Update character detail templates for each gameline
3. Update character form templates

### Phase 4: Locations App Templates

1. Update `locations/templates/locations/index.html`
2. Update location detail templates
3. Update location form templates

### Phase 5: Items App Templates

1. Update `items/templates/items/index.html`
2. Update item detail templates
3. Update item form templates

### Phase 6: Game App Templates

1. Update chronicle templates
2. Update scene templates
3. Update game form templates

### Phase 7: Accounts App Templates

1. Update profile templates
2. Update authentication templates

### Phase 8: Testing and Refinement

1. Visual testing across all pages
2. Accessibility testing
3. Responsive testing
4. Theme compatibility testing
5. Bug fixes and refinements

## Design Decisions and Rationales

### Decision 1: Component-First Approach

**Rationale**: Using the existing TG component library ensures consistency and makes future maintenance easier. Rather than creating new components, we enhance existing ones.

### Decision 2: Minimal CSS Additions

**Rationale**: Adding to existing CSS files rather than creating new ones keeps the codebase organized and prevents CSS bloat. All new styles are logical extensions of existing patterns.

### Decision 3: Template Updates In-Place

**Rationale**: Updating existing templates rather than creating new ones maintains the existing file structure and makes the changes easier to review and test.

### Decision 4: Gameline Font Application via CSS Classes

**Rationale**: Using CSS classes like `vtm_heading`, `wta_heading`, etc. allows templates to declaratively specify gameline fonts without inline styles, making the approach maintainable and consistent.

### Decision 5: Mobile-First Responsive Design

**Rationale**: Starting with mobile layouts ensures the site works well on all devices and follows modern web development best practices.

### Decision 6: Preserve Bootstrap Grid

**Rationale**: The existing Bootstrap grid system works well and is familiar to developers. We enhance it with custom components rather than replacing it.

### Decision 7: CSS Custom Properties for Theming

**Rationale**: The existing CSS custom property system is robust and well-designed. We extend it rather than creating a new theming approach.

### Decision 8: Progressive Enhancement

**Rationale**: Ensuring the site works without JavaScript and with basic CSS support makes it more accessible and resilient.
