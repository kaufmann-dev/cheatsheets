---
version: alpha
name: Aether
description: >
  A warm minimalist design system for content-focused websites. Grayscale foundation
  with subtle atmospheric gradients, sharp typography, and purposeful restraint.
colors:
  primary: '#000000'
  on-primary: '#ffffff'
  surface: '#fafafa'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1a1a'
  on-surface-variant: '#555555'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f0f1f1'
  outline: '#747878'
  outline-variant: '#c4c7c7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  gradient-warm: '#ff2550'
  gradient-cool: '#55CDFC'
typography:
  headline-xl:
    fontFamily: Google Sans Flex
    fontSize: 2.5rem
    fontWeight: 700
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Google Sans Flex
    fontSize: 1.5rem
    fontWeight: 600
  headline-md:
    fontFamily: Google Sans Flex
    fontSize: 1.125rem
    fontWeight: 500
  body-lg:
    fontFamily: Google Sans Flex
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.6
  body-md:
    fontFamily: Google Sans Flex
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  label-md:
    fontFamily: Google Sans Flex
    fontSize: 0.9375rem
    fontWeight: 500
  label-sm:
    fontFamily: Google Sans Flex
    fontSize: 0.75rem
    fontWeight: 400
rounded:
  sm: 5px
  md: 5px
  lg: 5px
  full: 40px
spacing:
  xs: 6px
  sm: 8px
  md: 10px
  lg: 15px
  xl: 20px
  2xl: 24px
  3xl: 30px
  4xl: 40px
  5xl: 100px
  gutter: 20px
  container-max: 80ch
components:
  button-primary:
    backgroundColor: '{colors.primary}'
    textColor: '{colors.on-primary}'
    rounded: '{rounded.sm}'
    padding: 6px 12px
  button-primary-hover:
    backgroundColor: '{colors.on-surface-variant}'
  tag:
    backgroundColor: '#0d000000'
    textColor: '{colors.on-surface-variant}'
    rounded: '{rounded.sm}'
    padding: 3px 7px
  navbar:
    backgroundColor: '#ccfafafa'
    height: 56px
  card:
    backgroundColor: '{colors.surface}'
    padding: 24px
---

# Aether — Design System

> A warm minimalist design system for content-focused websites. Grayscale foundation with subtle atmospheric gradients, sharp typography, and purposeful restraint.

---

## Brand & Style

### Core Identity

This design system communicates:

- **Technical competence** — clean structure, sharp typography, precision in spacing
- **Approachability** — generous whitespace, smooth transitions, warm atmospheric color
- **Confidence without arrogance** — no heavy gradients, no neon, no excessive animation

### Design Direction

The visual direction sits at the intersection of **minimalist functionalism** and **subtle warmth**:

- **Information architecture first** — content hierarchy drives every decision
- **Grayscale foundation** — black, white, and grays form the base; color is used sparingly as ambient atmosphere
- **Precision in restraint** — every element earns its place; no decorative filler
- **Motion with purpose** — transitions are smooth but never performative

### Temperament

| Attribute      | Value                                     |
| -------------- | ----------------------------------------- |
| Density        | Medium — breathable but not sparse        |
| Temperature    | Cool-neutral with warm undertones         |
| Personality    | Professional, understated, precise        |
| Visual weight  | Light — high background-to-ink contrast   |

---

## Colors

### Palette

The palette is anchored by a high-contrast relationship between warm off-white (`{colors.surface}`) and pure black (`{colors.primary}`).

- **Primary ({colors.primary}):** Used for buttons, links, interactive elements, and h1 headings. The sole driver of visual authority.
- **On-Surface ({colors.on-surface}):** Deep ink for headings and primary text. Nearly black but subtly softened.
- **On-Surface-Variant ({colors.on-surface-variant}):** Body text, descriptions, and secondary labels. Provides comfortable reading contrast without the intensity of full black.
- **Surface ({colors.surface}):** Warm off-white page background. Softer than pure white, reduces eye strain.
- **Outline ({colors.outline}) / Outline-Variant ({colors.outline-variant}):** Structural borders and dividers at varying emphasis levels.
- **Error ({colors.error}):** Reserved for validation and error states.

### Gradient Atmosphere

The background is a **4-layer stack**:

1. **Base**: `{colors.surface}` warm off-white
2. **Vertical fade**: Gradient to transparent in the middle, fading back to `{colors.surface}` at top and bottom
3. **Pink glow**: Radial gradient at `120% 60%`, `gradient-warm` at 30% opacity — soft sunset warmth
4. **Blue glow**: Radial gradient at `-20% 60%`, `gradient-cool` at 30% opacity — cool counterbalance

```css
:root {
    --background: linear-gradient(to bottom, {colors.surface} 0%, transparent 30%, transparent 70%, {colors.surface} 100%),
        radial-gradient(ellipse at 120% 60%, {colors.gradient-warm}30 0%, transparent 60%),
        radial-gradient(ellipse at -20% 60%, {colors.gradient-cool}50 0%, transparent 60%),
        {colors.surface};
}
```

> These gradients are extremely subtle and serve as **ambient atmosphere**, not decoration. They prevent the page from feeling sterile without introducing oversaturated gradient backgrounds.

### Selection & Scrollbar

- **Selection**: `background: on-surface; color: on-primary;` — inverted high contrast
- **Scrollbar**: Thin, `6px` width, `on-surface-variant` thumb on `surface` track, rounded

---

## Typography

The type system uses a single family — **Google Sans Flex** — across all contexts. Its optical size axis ensures sharp rendering at every scale, from large headlines to small captions.

- **Headlines** (`headline-xl`, `headline-lg`, `headline-md`): Heavy weights (500–700) with tight letter-spacing create strong visual anchors. `headline-xl` uses negative tracking for an editorial feel.
- **Body** (`body-lg`, `body-md`): Regular weight at 1.6 line height optimizes for comfortable long-form reading.
- **Labels** (`label-md`, `label-sm`): Medium weight, slightly smaller sizes for tags, nav links, captions, and metadata.

### Principles

- **No decorative icons per heading** — inline SVG icons belong inside buttons, not as bullet decorators
- **Word break**: `break-word` on headlines for long strings; `keep-all` on list items
- **Text wrap**: Natural flow, no forced truncation except in constrained containers (use `white-space: nowrap; text-overflow: ellipsis` when needed)

---

## Layout & Spacing

### Container System

- **Max content width**: `80ch` (~640–720px depending on font) — optimal reading measure
- **Page padding**: `{spacing.xl}` (20px) horizontal, `{spacing.5xl}` (100px) top (accounts for fixed navbar), `{spacing.3xl}` (30px) bottom
- **Content container**: Flex column, centered, with `flex: 1`
- **Content child**: Max-width constrained, fade-in-up entrance animation

### Grid Patterns

**Image Grid**:
- Mobile: `repeat(2, 1fr)`
- Tablet (≥640px): `repeat(3, 1fr)`
- Desktop (≥1024px): `repeat(4, 1fr)`
- Gap: `{spacing.xl}` (20px)

**Card List**:
- Single column layout
- Gap: `{spacing.md}` (10px)
- Separators: `5px solid {colors.outline-variant}` between items, `{spacing.3xl}` (30px) padding-bottom

**Horizontal Card Row**:
- Desktop: Horizontal flex, `{spacing.2xl}` (24px) gap, image 250px fixed width
- Mobile (≤768px): Stacks vertically, image 100% width

### Responsive Breakpoints

| Name              | Width          | Changes                                                                    |
| ----------------- | -------------- | -------------------------------------------------------------------------- |
| **Mobile**        | ≤600px         | Hamburger nav, fullscreen menu, single column cards, 2-col image grid      |
| **Tablet**        | 640px–1023px   | 3-col image grid                                                           |
| **Desktop**       | ≥1024px        | 4-col image grid, horizontal card layout                                   |
| **Card stack**    | ≤768px         | Cards stack vertically (image above content)                               |

---

## Elevation & Depth

This design system rejects traditional shadows in favor of **Tonal Layers** and **Structural Borders**. Depth is communicated through layering rather than atmospheric effects.

- **Surfaces**: Use subtle shifts between `surface` and `surface-container-lowest` to indicate elevation.
- **Outlines**: Very subtle `1px` borders using `outline-variant` at low opacity define component boundaries. High-emphasis items may use a solid `primary` border.
- **Interactions**: On hover, elements transition colors smoothly (e.g., background to `on-surface-variant`). The subtle button shine effect adds life without adding depth.

---

## Shapes

The shape language is **Sharp with Minimal Softening**.

Corners use a consistent `rounded.sm` (5px) across buttons, tags, images, and media containers. This communicates precision and technical focus while avoiding both the harshness of 0px corners and the overused "rounded card slop" look. There are no pill shapes on content elements.

- **Nav links**: Use `rounded.full` (40px) — an intentional exception to soften navigation and create clear active-state containers.
- **Avatars**: Squircle via SVG mask — friendlier than a circle, more distinctive than a rounded rectangle.

---

## Components

### Navigation (Navbar)

**Desktop**:
- Fixed top, full width, `z-index: 100`
- Background: `navbar.backgroundColor` with `backdrop-filter: blur(12px)`
- Border-bottom: `1px solid outline-variant`
- Shadow: `0 4px 20px -10px rgba(0,0,0,0.05)`
- Links centered, pill-shaped (`rounded.full`), `lg` gap between items
- Link hover: color transitions to `on-surface`
- Active state: `color: on-surface; font-weight: 600;`

**Mobile** (≤600px):
- Hamburger button: 2 bars, 24px wide, 2px height, animated to X on open
- Full-screen overlay menu: 100vw × 100vh, centered flex column
- Background: `navbar.backgroundColor` with `blur(20px)`
- Links: `headline-lg` size, `600` weight, larger touch targets
- Entrance: `opacity 0 → 1`, `translateY(-20px) → 0`, `0.4s` ease

**Hamburger Animation**:
```css
.bar:nth-child(1) { transform: translateY(4px) rotate(45deg); }
.bar:nth-child(2) { transform: translateY(-4px) rotate(-45deg); }
```
Easing: `cubic-bezier(0.175, 0.885, 0.32, 1.275)` — bouncy, organic

### Buttons & CTAs

**Primary Button** (`button-primary`):
- Background: `{colors.primary}`
- Text: `{colors.on-primary}`
- Padding: `button-primary.padding`
- Border-radius: `{rounded.sm}`
- Hover: background transitions to `{colors.on-surface-variant}`
- **Shine effect**: Pseudo-element with animated gradient sweep (3s infinite loop)

```css
button::before {
    content: '';
    position: absolute;
    top: 0; left: -150%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.1) 40%, rgba(255,255,255,0.3) 50%, rgba(255,255,255,0.1) 60%, transparent 100%);
    animation: highlightSlide 3s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
```

**Button Icon**:
- 20px × 20px, `fill: currentColor`
- Placed after text with `sm` gap

### Content Card

```
┌─────────────────────────────────────────┐
│ ┌─────────┐  ┌────────────────────────┐ │
│ │ Image   │  │ Title          [Button]│ │
│ │ (250px) │  │ Subtitle               │ │
│ │         │  │ — Detail point         │ │
│ └─────────┘  │ — Detail point         │ │
│              │ [Tag] [Tag] [Tag]       │ │
│              └────────────────────────┘ │
└─────────────────────────────────────────┘
```

- Image: 250px fixed width desktop, 100% mobile
- Content area: `flex: 1`, `min-width: 0` (prevents flex overflow)
- Title row: heading + action button aligned to opposite ends (flex, space-between)
- Subtitle: displayed below title in `on-surface-variant`
- List items: prefixed with em-dash (`—`), not standard bullets
- Tags: displayed below detail points in a flex-wrap row
- Responsive: Stacks vertically below 768px
- Separators: `5px solid outline-variant` between cards

### Tags

- Background: `tag.backgroundColor` (5% black overlay)
- Text: `{colors.on-surface-variant}`
- Padding: `tag.padding`
- Border-radius: `{rounded.sm}`
- Typography: `label-md`
- Container: flex wrap, `sm` gap
- Extremely subtle — nearly monochrome, no borders

### Avatar

- Size: 100px × 100px
- Shape: **Squircle** via SVG mask
- Hover: `transform: scale(1.05)`
- Transition: `0.3s cubic-bezier(0.4, 0, 0.2, 1)`

### Media Containers

**Image Container**:
- Background: `surface-container` at low opacity
- Border-radius: `{rounded.sm}`
- Overflow: hidden
- Image max-width: 500px, centered

**Video**: Same constraints as images

### Animation & Motion

**Entrance**:
```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
```
- Duration: `0.8s`, easing: `cubic-bezier(0.4, 0, 0.2, 1)`

**Button Shine**:
```css
@keyframes highlightSlide {
    0%   { left: -150%; }
    50%  { left: 150%; }
    100% { left: -150%; }
}
```
- Duration: `3s`, easing: `cubic-bezier(0.4, 0, 0.2, 1)`, loop: infinite

**Hover Transitions**:

| Element           | Property           | Duration | Easing                                       |
| ----------------- | ------------------ | -------- | -------------------------------------------- |
| Links             | `color`            | `0.3s`   | `cubic-bezier(0.4, 0, 0.2, 1)`              |
| Buttons           | `background-color` | `0.3s`   | `cubic-bezier(0.4, 0, 0.2, 1)`              |
| Avatars           | `transform`        | `0.3s`   | `cubic-bezier(0.4, 0, 0.2, 1)`              |
| Nav links         | `all`              | `0.2s`   | `ease`                                       |
| Mobile menu       | `all`              | `0.4s`   | `cubic-bezier(0.175, 0.885, 0.32, 1.275)`   |

### Accessibility

- **Focus states**: `outline: 2px solid on-surface-variant; outline-offset: 2px;` on buttons and links
- **ARIA**: Hamburger button requires `aria-label="Toggle navigation"` and `aria-expanded` state
- **Reduced motion**: Entrance animations should degrade gracefully; consider `prefers-reduced-motion` media query
- **Semantic HTML**: Use `<header>`, `<nav>`, `<main>`, `<figure>`, `<figcaption>` correctly
- **Lazy loading**: Card images should use `loading="lazy"`
- **Alt text**: All images require descriptive alt text

### Asset Guidelines

**Images**:

| Type             | Format | Max Width           | Notes                       |
| ---------------- | ------ | ------------------- | --------------------------- |
| Card thumbnails  | WebP   | ~570–615px          | Dual srcset for responsive  |
| Content images   | WebP   | 500px displayed     | Centered in container       |
| Portrait/Avatar  | WebP   | 100px displayed     | Squircle mask applied       |
| Favicon          | ICO    | Standard            | Plus `apple-touch-icon.png` |

**Icons**:
- Source: Inline SVG
- Size: 20px × 20px
- Color: `currentColor` — inherits from parent
- Placement: Inside buttons, alongside text with flex gap

---

## Do's and Don'ts

- **Do** use the grayscale foundation as the primary visual language; let content imagery provide color
- **Do** use subtle atmospheric gradients (pink/blue radial glows) for background warmth
- **Do** use `5px` border-radius consistently across buttons, tags, images, and containers
- **Do** use em-dash (`—`) list markers for editorial, non-generic aesthetics
- **Do** place heading and CTA button on the same row for efficient scanning
- **Do** maintain a single global CSS file for simple, content-focused sites
- **Do** use `80ch` max-width for optimal reading measure
- **Don't** use purple/blue gradient hero backgrounds — generic and overused
- **Don't** use emoji as bullet icons — looks unprofessional in technical contexts
- **Don't** apply heavy drop shadows on cards — contradicts the light, flat aesthetic
- **Don't** use rounded cards with left accent borders — component-library cliché
- **Don't** add decorative stats or quotes sections — every element must earn its place
- **Don't** use a multi-color tag system — introduces unnecessary chromatic noise
- **Don't** use monospaced body text — reduces readability; reserve for code blocks only
- **Don't** implement dark mode as a simple color inversion — the gradient atmosphere is integral to the identity
