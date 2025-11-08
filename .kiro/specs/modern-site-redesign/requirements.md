# Requirements Document

## Introduction

This specification defines the requirements for redesigning the Tellurium Games World of Darkness site with a modern, consistent visual design system. The redesign will update existing templates across all Django apps (characters, locations, items, game, accounts, core) to use a unified component-based approach with attractive color palettes that work seamlessly with the existing theme system (light/dark modes). The redesign will maintain all existing functionality while improving visual consistency, accessibility, and user experience. Gameline-specific fonts will be consistently applied to appropriate content throughout the site.

## Glossary

- **Site**: The Tellurium Games World of Darkness Django web application
- **Template**: Django HTML template files that render pages in the application
- **Theme System**: The existing CSS custom property-based theming infrastructure supporting light and dark modes
- **Component Library**: The existing TG-prefixed CSS component system (tg-card, tg-btn, tg-badge, etc.)
- **Gameline**: A specific World of Darkness game system (VTM=Vampire, WTA=Werewolf, MTA=Mage, CTD=Changeling, WTO=Wraith)
- **Gameline Font**: Specific decorative fonts associated with each gameline (Delavan for VTM, Balthazar for WTA, Abbess for MTA, Kells for CTD, MatrixTall for WTO)
- **App**: A Django application module (characters, locations, items, game, accounts, core)
- **Color Palette**: The coordinated set of colors used throughout the site that work with both light and dark themes
- **Bootstrap**: The Bootstrap 4 CSS framework currently used for layout and components

## Requirements

### Requirement 1

**User Story:** As a site visitor, I want a modern and visually appealing interface, so that the site feels professional and engaging to use.

#### Acceptance Criteria

1. WHEN a user views any page on the Site, THE Site SHALL display content using a consistent modern design language with appropriate spacing, typography, and visual hierarchy
2. WHEN a user views any page on the Site, THE Site SHALL apply color palettes that provide sufficient contrast and visual appeal in both light and dark themes
3. WHEN a user views any page on the Site, THE Site SHALL display interactive elements (buttons, cards, links) with smooth transitions and hover effects
4. WHEN a user views content on mobile devices, THE Site SHALL display responsive layouts that adapt appropriately to different screen sizes
5. WHEN a user views gameline-specific content, THE Site SHALL display headings and titles using the appropriate Gameline Font for that content type

### Requirement 2

**User Story:** As a site administrator, I want all templates to use the existing component library consistently, so that maintenance is simplified and design changes can be applied globally.

#### Acceptance Criteria

1. WHEN templates are updated, THE Site SHALL use TG-prefixed component classes (tg-card, tg-btn, tg-badge) instead of inline styles or mixed Bootstrap classes
2. WHEN templates are updated, THE Site SHALL remove inline style blocks from template files where component classes can be used instead
3. WHEN templates are updated, THE Site SHALL maintain all existing functionality including forms, navigation, data display, and user interactions
4. WHEN templates are updated, THE Site SHALL use the existing Theme System CSS custom properties for colors, spacing, and typography
5. WHEN a developer needs to make design changes, THE Site SHALL allow modifications through the centralized component CSS files rather than individual templates

### Requirement 3

**User Story:** As a site user, I want consistent visual design across all sections of the site, so that navigation feels intuitive and the experience is cohesive.

#### Acceptance Criteria

1. WHEN a user navigates between different Apps, THE Site SHALL display consistent card layouts, button styles, and typography across all sections
2. WHEN a user views list pages (character index, location index, item index), THE Site SHALL display consistent table or card-based layouts with uniform spacing and styling
3. WHEN a user views detail pages (character detail, location detail, item detail), THE Site SHALL display consistent section headers, content organization, and action buttons
4. WHEN a user views forms (create, edit), THE Site SHALL display consistent form styling with proper labels, inputs, and validation feedback
5. WHEN a user views navigation elements, THE Site SHALL display consistent menu styling, breadcrumbs, and page headers across all Apps

### Requirement 4

**User Story:** As a content creator, I want gameline-specific content to be visually distinguished with appropriate fonts, so that different game systems are immediately recognizable.

#### Acceptance Criteria

1. WHEN a user views a Vampire (VTM) character, location, or item, THE Site SHALL display headings using the Delavan font
2. WHEN a user views a Werewolf (WTA) character, location, or item, THE Site SHALL display headings using the Balthazar font
3. WHEN a user views a Mage (MTA) character, location, or item, THE Site SHALL display headings using the Abbess font
4. WHEN a user views a Changeling (CTD) character, location, or item, THE Site SHALL display headings using the Kells font
5. WHEN a user views a Wraith (WTO) character, location, or item, THE Site SHALL display headings using the MatrixTall font
6. WHEN a user views mixed gameline content, THE Site SHALL apply the appropriate Gameline Font to each item's heading based on its gameline association

### Requirement 5

**User Story:** As a site user, I want the color scheme to be attractive and readable in both light and dark modes, so that I can use the site comfortably in any lighting condition.

#### Acceptance Criteria

1. WHEN a user enables light theme, THE Site SHALL display a Color Palette with warm, inviting colors that provide clear contrast and readability
2. WHEN a user enables dark theme, THE Site SHALL display a Color Palette with adjusted colors that maintain visual hierarchy and reduce eye strain
3. WHEN a user views interactive elements in either theme, THE Site SHALL display hover states and focus indicators with appropriate color changes
4. WHEN a user views gameline-specific content, THE Site SHALL display accent colors that complement the Gameline Font and theme mode
5. WHEN a user views status indicators (active, inactive, deceased), THE Site SHALL display colors that clearly communicate state in both theme modes

### Requirement 6

**User Story:** As a site developer, I want minimal new files created during the redesign, so that the codebase remains maintainable and doesn't become bloated.

#### Acceptance Criteria

1. WHEN the redesign is implemented, THE Site SHALL reuse existing CSS files (master-theme.css, components.css, theme-system.css) rather than creating new stylesheets
2. WHEN the redesign is implemented, THE Site SHALL update existing template files in place rather than creating duplicate templates
3. WHEN new CSS rules are needed, THE Site SHALL add them to existing component or theme files in the appropriate location
4. WHEN template updates are made, THE Site SHALL preserve existing template inheritance structure and block definitions
5. WHEN the redesign is complete, THE Site SHALL have no more than 2 new CSS files created (if absolutely necessary for specific redesign features)

### Requirement 7

**User Story:** As a site user with accessibility needs, I want the redesigned site to meet accessibility standards, so that I can navigate and use all features effectively.

#### Acceptance Criteria

1. WHEN a user navigates using keyboard only, THE Site SHALL provide visible focus indicators on all interactive elements
2. WHEN a user uses a screen reader, THE Site SHALL provide appropriate ARIA labels and semantic HTML structure
3. WHEN a user views text content, THE Site SHALL maintain a minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text
4. WHEN a user views interactive elements, THE Site SHALL provide touch targets of at least 44x44 pixels on mobile devices
5. WHEN a user enables reduced motion preferences, THE Site SHALL minimize or disable animations and transitions

### Requirement 8

**User Story:** As a site administrator, I want the redesign to maintain backward compatibility with existing data and functionality, so that no content or features are lost during the update.

#### Acceptance Criteria

1. WHEN templates are updated, THE Site SHALL preserve all existing Django template tags, filters, and context variables
2. WHEN templates are updated, THE Site SHALL maintain all existing form submissions, validations, and error handling
3. WHEN templates are updated, THE Site SHALL preserve all existing URL routing and navigation links
4. WHEN templates are updated, THE Site SHALL maintain all existing user permissions and access controls
5. WHEN the redesign is deployed, THE Site SHALL display all existing database content correctly without data migration
