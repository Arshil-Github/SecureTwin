---
name: Editorial Noir Glass
colors:
  surface: '#0d1512'
  surface-dim: '#0d1512'
  surface-bright: '#333b38'
  surface-container-lowest: '#08100d'
  surface-container-low: '#151d1b'
  surface-container: '#19211f'
  surface-container-high: '#232c29'
  surface-container-highest: '#2e3734'
  on-surface: '#dce5e0'
  on-surface-variant: '#b9cac3'
  inverse-surface: '#dce5e0'
  inverse-on-surface: '#2a322f'
  outline: '#84948e'
  outline-variant: '#3b4a45'
  surface-tint: '#00e0bb'
  primary: '#70ffdd'
  on-primary: '#00382d'
  primary-container: '#00e5c0'
  on-primary-container: '#006150'
  inverse-primary: '#006b59'
  secondary: '#ffb77c'
  on-secondary: '#4d2600'
  secondary-container: '#d57a1b'
  on-secondary-container: '#432100'
  tertiary: '#ffe4bc'
  on-tertiary: '#422c00'
  tertiary-container: '#ffc14e'
  on-tertiary-container: '#724f00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#42fdd7'
  primary-fixed-dim: '#00e0bb'
  on-primary-fixed: '#002019'
  on-primary-fixed-variant: '#005142'
  secondary-fixed: '#ffdcc2'
  secondary-fixed-dim: '#ffb77c'
  on-secondary-fixed: '#2e1500'
  on-secondary-fixed-variant: '#6d3900'
  tertiary-fixed: '#ffdeaa'
  tertiary-fixed-dim: '#f9bc49'
  on-tertiary-fixed: '#271900'
  on-tertiary-fixed-variant: '#5f4100'
  background: '#0d1512'
  on-background: '#dce5e0'
  surface-variant: '#2e3734'
typography:
  display-xl:
    fontFamily: Epilogue
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Epilogue
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  body-md:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  container-padding: 24px
  card-gap: 20px
---

## Brand & Style

This design system targets a high-net-worth, tech-savvy audience through an **Editorial Dark Luxury** aesthetic. The interface prioritizes an immersive, cinematic experience that feels both prestigious and technologically advanced. 

The style is a sophisticated blend of **Glassmorphism** and **High-Contrast Minimalism**. By placing vibrant, multi-dimensional gradients against a deep, ink-black void, we create a sense of infinite depth. The UI should evoke a "digital vault" feeling—secure, exclusive, and fluid. Use high-fidelity glass effects not just for decoration, but to establish a clear hierarchy of information layers.

## Colors

The foundation is **Ink Black (#080C14)**, providing a pure, high-contrast canvas. 

- **Primary & Secondary:** Electric Teal and Ember Amber are reserved strictly for functional indicators (status, success, warnings) and micro-interactions.
- **Card Gradients:** Use ultra-vibrant, wide-gamut gradients for primary data containers. These should feel luminous, as if backlit.
- **Neutral Palette:** Grays are blue-tinted to maintain the "Ink" temperature, preventing the UI from feeling "muddy" or flat gray.

## Typography

The typography system pairs **Epilogue** for high-impact editorial moments with **Manrope** for technical UI clarity.

- **Editorial Impact:** Use Epilogue for large headlines with tight letter-spacing to create a bold, "magazine" feel.
- **UI Legibility:** Manrope provides the necessary balance for data-heavy sections, maintaining a modern, refined tone without distracting from the card visuals.
- **Hierarchy:** Lean heavily on font-weight and size contrasts rather than color shifts to guide the eye.

## Layout & Spacing

The layout utilizes a **fluid grid** with generous internal margins to support the luxury narrative. 

- **Rhythm:** A strict 4px/8px baseline grid ensures vertical alignment.
- **Negative Space:** Embrace wide "breathable" areas around major card components. Content should never feel cramped; if in doubt, increase the `xl` spacing between sections.
- **Margins:** Standard mobile and desktop views use a minimum 24px side margin to separate content from the edge of the device.

## Elevation & Depth

Depth in this system is achieved through **Glassmorphism** rather than traditional drop shadows.

- **The Glass Layer:** Use `backdrop-filter: blur(20px)` combined with a semi-transparent fill (`rgba(255, 255, 255, 0.05)`). 
- **The Border:** Every card and floating element must have a 1px solid border. Use a top-down linear gradient for the border (e.g., `rgba(255,255,255,0.2)` at the top to `rgba(255,255,255,0.05)` at the bottom) to simulate a light catch on the edge.
- **Shadows:** Use large, ultra-diffused "Ambient" shadows with very low opacity (10-15%) and a slight color tint matching the card's primary gradient color.

## Shapes

The shape language is defined by **ROUND_L** (Level 2).

- **Outer Containers:** Large cards and primary buttons use a 1.5rem (24px) radius.
- **Nested Elements:** Small buttons or tags within cards should use a 0.5rem (8px) radius to create a nested "squircle" harmony.
- **Consistency:** Avoid sharp corners entirely to maintain the fluid, organic feel of the glass elements.

## Components

- **Cards:** The hero of the UI. Cards should feature a "frosted" footer area for text and a vibrant gradient header or background. Interaction should trigger a subtle scale-up and increased glow effect.
- **Buttons:** Primary buttons use a mesh gradient fill with white text. Secondary buttons should be "Ghost Glass"—transparent with a 1px border and blur.
- **Chips/Tags:** Small, pill-shaped elements with high-transparency backgrounds. Use Ember Amber and Electric Teal sparingly here for status.
- **Inputs:** Minimalist bottom-border only or very subtle dark-filled glass containers. Focus state is indicated by the 1px border glowing in Electric Teal.
- **Navigation:** A floating "Glass Dock" at the bottom of the screen, utilizing heavy backdrop blur and centered icons.