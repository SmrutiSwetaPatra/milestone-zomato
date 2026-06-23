---
name: Epicurean Intelligence
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#5b403d'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#8f6f6c'
  outline-variant: '#e4beba'
  surface-tint: '#ba1a20'
  primary: '#af101a'
  on-primary: '#ffffff'
  primary-container: '#d32f2f'
  on-primary-container: '#fff2f0'
  inverse-primary: '#ffb3ac'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfde'
  on-secondary-container: '#636262'
  tertiary: '#565858'
  on-tertiary: '#ffffff'
  tertiary-container: '#6e7070'
  on-tertiary-container: '#f4f4f4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad6'
  primary-fixed-dim: '#ffb3ac'
  on-primary-fixed: '#410003'
  on-primary-fixed-variant: '#930010'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '500'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  container-max: 1200px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

The design system is built for a premium, AI-driven restaurant recommendation experience. The brand personality is sophisticated, decisive, and hyper-clean, aiming to reduce the cognitive load of choosing a dining location. It targets discerning users who value efficiency and high-quality curation over endless scrolling.

The visual style is **High-End Minimalism**. It leverages a "Gallery" aesthetic—where the UI recedes into the background to let food photography and AI insights take center stage. Key characteristics include expansive whitespace, razor-sharp typography, and a restrained use of a high-impact crimson accent to denote passion and culinary excellence.

## Colors

The palette is anchored in a high-contrast, "paper-white" environment.

*   **Primary (#D32F2F):** A deep, authoritative crimson used exclusively for calls to action, active states, and brand-heavy highlights.
*   **Surface (#F9F9F9):** An off-white used to define secondary containers, input backgrounds, and card surfaces against the pure white (#FFFFFF) page background.
*   **Text Hierarchy:** 
    *   **High-Contrast Slate (#1A1A1A):** Used for primary headings and body text to ensure maximum legibility.
    *   **Medium Slate (#64748B):** Used for metadata, labels, and secondary information.
*   **Success/Error:** Use standard semantic greens for success, while the primary crimson doubles as the error indicator to maintain the minimalist aesthetic.

## Typography

The design system utilizes **Inter** across all levels to maintain a systematic, modern, and utilitarian feel. 

*   **Headings:** Use bold weights (700) with slight negative letter-spacing to create a "locked-in" editorial look.
*   **Body:** Body text is kept at a medium weight (500) for standard readability and a slightly more "premium" feel than regular weights.
*   **Labels:** Small metadata and labels should use uppercase styling with increased letter spacing for a refined, architectural touch.

## Layout & Spacing

This design system follows a **Fluid-to-Fixed Grid** model. 
*   **Desktop:** 12-column grid with a maximum width of 1200px to ensure the UI feels intimate and curated rather than stretched.
*   **Mobile:** 4-column grid with 16px side margins. 
*   **Rhythm:** An 8px base unit drives all padding and margin decisions. Deep vertical whitespace (64px+) should be used between major sections to emphasize the minimalist "Clean UI" philosophy.

## Elevation & Depth

Visual hierarchy is achieved through subtle tonal shifts and soft shadows rather than heavy borders or colors.

*   **Base Layer:** Pure White (#FFFFFF).
*   **Surface Layer:** Off-White (#F9F9F9) for card backgrounds and input fields.
*   **Shadows:** Use a "Natural Ambient" shadow for cards: `0px 12px 32px rgba(0, 0, 0, 0.04)`. The shadow should be barely perceptible, serving only to lift the card off the background.
*   **Active States:** On hover, elevation should increase by doubling the shadow opacity and shifting the element up by 2px.

## Shapes

The design system uses **Soft (1)** roundedness. 
*   **Standard Elements:** 4px (0.25rem) for buttons and inputs.
*   **Cards:** 8px (0.5rem) for restaurant cards and highlight blocks.
*   **Images:** Always match the container corner radius to maintain a clean, nested appearance. 
*   **Pills:** Tags or categories should use a fully rounded (pill) shape to contrast against the structured rectangular inputs.

## Components

### Buttons
Primary buttons are solid Crimson (#D32F2F) with white text. Secondary buttons use a 1px border of Slate (#64748B) with a transparent background. Interaction involves a subtle `scale(0.98)` on click to provide tactile feedback.

### Inputs
Search and filter inputs are horizontal, spanning the full width of their container where possible. They feature a 1px border (#E2E8F0) and an off-white background (#F9F9F9). On focus, the border transitions to Crimson.

### Restaurant Cards
Cards are oriented horizontally. The left side features a high-resolution 1:1 image. The right side contains the restaurant name, star rating (using the Star Selector component), and a dedicated **AI Explanation Block**.
*   **AI Explanation Block:** A subtly tinted box within the card (using 5% Crimson opacity) that highlights "Why this matches you" in `body-md` typography.

### Star Rating Selectors
Ratings use a custom geometric star icon. Selected stars are solid Crimson; unselected stars are a light gray stroke.

### Lists
Lists should be "Airy," with significant vertical padding (24px) between items and a thin, 1px light gray separator that doesn't touch the edges of the container.