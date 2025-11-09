# Implementation Plan

- [x] 1. Enhance CSS theme system and components
  - Add enhanced color palette variables to theme-system.css including accent colors, status colors, gameline light variants, and interactive state colors
  - Add page header component styles to components.css with gameline-specific styling
  - Add enhanced table component styles to components.css with responsive mobile layout
  - Add enhanced form component styles to components.css including validation states
  - Add enhanced navigation tab styles to components.css with mobile-responsive behavior
  - Add error/warning/info/success message styles to components.css
  - _Requirements: 1.1, 1.2, 1.3, 2.4, 5.1, 5.2, 5.3_

- [x] 2. Update core app templates
  - Update core/templates/core/index.html to use tg-card components and standardized page header pattern
  - Update core/templates/core/form.html to use enhanced tg-form components
  - Review core/templates/core/base.html for any needed consistency improvements
  - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.4, 8.1, 8.2_

- [x] 3. Update characters app index template
  - Update characters/templates/characters/index.html to use tg-card components
  - Replace inline styles with tg-nav-tabs component classes
  - Apply standardized page header with gameline font support
  - Update character list display to use tg-table or enhanced card layout
  - Ensure status badges use tg-badge component classes
  - _Requirements: 1.1, 1.5, 2.1, 2.2, 3.1, 3.2, 4.6, 5.5_

- [ ] 4. Update characters app detail templates
  - Update vampire character detail template to use tg-card sections and vtm_heading class
  - Update werewolf character detail template to use tg-card sections and wta_heading class
  - Update mage character detail template to use tg-card sections and mta_heading class
  - Update changeling character detail template to use tg-card sections and ctd_heading class
  - Update wraith character detail template to use tg-card sections and wto_heading class
  - Ensure consistent section organization across all character types
  - Apply gameline-specific data-gameline attributes to header cards
  - _Requirements: 1.1, 1.5, 2.1, 3.1, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 5. Update characters app form templates
  - Update character creation forms to use tg-form-group and tg-form-control classes
  - Update character edit forms to use enhanced form components
  - Ensure form validation feedback uses tg-form-feedback classes
  - Apply consistent button styling with tg-btn classes
  - _Requirements: 2.1, 2.2, 3.4, 8.2_

- [x] 6. Update locations app index template
  - Update locations/templates/locations/index.html to use tg-card and tg-nav-tabs components
  - Replace inline styles with tg-nav-tabs component classes
  - Apply standardized page header with gameline font support
  - Update location list display to use tg-table with collapsible hierarchy
  - Ensure type badges use tg-badge component classes with gameline-specific colors
  - Update create location form to match character index styling
  - _Requirements: 1.1, 1.5, 2.1, 2.2, 3.1, 3.2, 4.6, 5.5_

- [x] 7. Update locations app detail templates





  - Update location detail template to use tg-card sections
  - Update city location detail template to use tg-card sections
  - Update chantry location detail template to use tg-card sections and mta_heading class
  - Update node location detail template to use tg-card sections and mta_heading class
  - Update library location detail template to use tg-card sections and mta_heading class
  - Update sector location detail template to use tg-card sections and mta_heading class
  - Update realm location detail template to use tg-card sections and mta_heading class
  - Update sanctum location detail template to use tg-card sections and mta_heading class
  - Update caern location detail template to use tg-card sections and wta_heading class
  - Update reality zone detail template to use tg-card sections
  - Ensure consistent section organization across all location types
  - Apply gameline-specific data-gameline attributes to header cards
  - _Requirements: 1.1, 1.5, 2.1, 3.1, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 8. Update locations app form templates
  - Update location creation forms to use tg-form-group and tg-form-control classes
  - Update location edit forms to use enhanced form components
  - Ensure form validation feedback uses tg-form-feedback classes
  - Apply consistent button styling with tg-btn classes
  - Update chantry creation wizard (locgen.html) to use enhanced components
  - _Requirements: 2.1, 2.2, 3.4, 8.2_

- [x] 9. Update items app index template
  - Update items/templates/items/index.html to use tg-card and tg-nav-tabs components
  - Replace inline styles with tg-nav-tabs component classes
  - Apply standardized page header with gameline font support
  - Update item list display to use tg-table or enhanced card layout
  - Ensure type badges use tg-badge component classes with gameline-specific colors
  - Update create item form to match character/location index styling
  - _Requirements: 1.1, 1.5, 2.1, 2.2, 3.1, 3.2, 4.6, 5.5_

- [ ] 10. Update items app detail templates
  - Update weapon detail templates to use tg-card sections
  - Update armor detail templates to use tg-card sections
  - Update fetish detail templates to use tg-card sections and wta_heading class
  - Update talisman detail templates to use tg-card sections and mta_heading class
  - Update wonder detail templates to use tg-card sections and ctd_heading class
  - Ensure consistent section organization across all item types
  - Apply gameline-specific data-gameline attributes to header cards
  - _Requirements: 1.1, 1.5, 2.1, 3.1, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 11. Update items app form templates
  - Update item creation forms to use tg-form-group and tg-form-control classes
  - Update item edit forms to use enhanced form components
  - Ensure form validation feedback uses tg-form-feedback classes
  - Apply consistent button styling with tg-btn classes
  - _Requirements: 2.1, 2.2, 3.4, 8.2_

- [ ] 12. Update game app templates
  - Update chronicle list and detail templates to use tg-card components
  - Update scene list and detail templates to use tg-card components
  - Update game-related forms to use enhanced tg-form components
  - Ensure consistent navigation and layout patterns
  - _Requirements: 2.1, 3.1, 3.3, 3.4_

- [x] 13. Update accounts app templates
  - Update profile templates to use tg-card components
  - Update login template to use enhanced tg-form components
  - Update signup template to use enhanced tg-form components
  - Update password reset templates to use enhanced tg-form components
  - Ensure theme selection interface is styled consistently
  - _Requirements: 2.1, 3.1, 3.4_

- [ ] 14. Perform visual and functional testing
  - Test all templates in light theme mode across Chrome, Firefox, Safari, Edge
  - Test all templates in dark theme mode across Chrome, Firefox, Safari, Edge
  - Test responsive layouts on mobile devices (iOS and Android)
  - Test responsive layouts on tablet devices
  - Verify gameline fonts display correctly for VTM, WTA, MTA, CTD, WTO content
  - Test all forms for proper submission and validation
  - Test all navigation elements and links
  - Verify theme switching works correctly
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 5.5, 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 15. Perform accessibility testing
  - Test keyboard navigation through all interactive elements
  - Verify visible focus indicators on all buttons, links, and form controls
  - Test with screen reader (NVDA, JAWS, or VoiceOver)
  - Verify ARIA labels and semantic HTML structure
  - Check color contrast ratios meet WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
  - Verify touch targets are at least 44x44 pixels on mobile
  - Test with reduced motion preferences enabled
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 16. Final review and refinement
  - Review all updated templates for consistency
  - Verify no inline styles remain where components can be used
  - Check that all templates maintain existing functionality
  - Verify backward compatibility with existing data
  - Document any new CSS classes or patterns added
  - Create summary of changes for deployment
  - _Requirements: 2.1, 2.2, 2.3, 2.5, 6.1, 6.2, 6.3, 6.4, 6.5, 8.1, 8.2, 8.3, 8.4, 8.5_
