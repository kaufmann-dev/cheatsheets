---
version: alpha
name: Technical Precision
description: Functional brutalism for developer tools. Monochrome foundation, typographic identity, engineering-grade clarity.
colors:
  primary: "#0070F3"
  on-primary: "#ffffff"
  background: "#FFFFFF"
  on-background: "#111111"
  surface-subtle: "#F5F5F7"
  border-subtle: "#EAEAEA"
  text-muted: "#666666"
  success: "#4ADE80"
  warning: "#FACC15"
  error: "#F87171"
typography:
  headline-xl:
    fontFamily: Geist Sans
    fontSize: 40px
    fontWeight: "700"
    lineHeight: "1.2"
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Geist Sans
    fontSize: 32px
    fontWeight: "700"
    lineHeight: "1.2"
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Geist Sans
    fontSize: 24px
    fontWeight: "600"
    lineHeight: "1.3"
    letterSpacing: -0.02em
  body-lg:
    fontFamily: Geist Sans
    fontSize: 18px
    fontWeight: "400"
    lineHeight: "1.6"
  body-md:
    fontFamily: Geist Sans
    fontSize: 14px
    fontWeight: "400"
    lineHeight: "1.5"
  code:
    fontFamily: Geist Mono
    fontSize: 13px
    fontWeight: "400"
    lineHeight: "1.6"
  label-caps:
    fontFamily: Geist Mono
    fontSize: 11px
    fontWeight: "600"
    lineHeight: "1"
    letterSpacing: 0.05em
spacing:
  unit: 4px
  gutter: 24px
  margin-edge: 32px
  container-max: 1200px
rounded:
  sm: 4px
  md: 8px
components:
  button-primary:
    backgroundColor: "{colors.on-background}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
    padding: "12px 16px"
    typography: "{typography.body-md}"
  button-ghost:
    backgroundColor: "{colors.background}"
    textColor: "{colors.on-background}"
    rounded: "{rounded.sm}"
    padding: "12px 16px"
    typography: "{typography.body-md}"
  button-danger:
    backgroundColor: "{colors.error}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.sm}"
    padding: "8px 12px"
    typography: "{typography.body-md}"
---

## Overview

This design system is engineered for high-performance utility and technical clarity. Drawing inspiration from Vercel's Geist system and modern developer tools, the aesthetic is rooted in **Minimalism** with a **Functional/Technical** edge.

The brand personality is authoritative yet unobtrusive, prioritizing content and data visualization over decorative elements. It evokes a sense of "Geist" — the spirit of precision — utilizing ample whitespace, a disciplined color palette, and high-quality monospaced accents to signify a developer-first environment. The interface should feel fast, responsive, and rigorously organized, catering to a professional audience that values efficiency and logical structure.

### Core Principles

1. **Speed as a Feature**: The design must feel "fast." No unnecessary animations. The interface prioritizes perceived performance.
2. **Text over Image**: Information is conveyed primarily through text and typography, not decorative imagery.
3. **Engineering Aesthetics**: Code snippets and terminal commands are prominent design elements, not afterthoughts.
4. **Content Density**: The system favors compact layouts with high information density, using whitespace strategically to establish hierarchy rather than fill space.
5. **Semantic Color**: Every color in the palette must carry functional meaning. Decorative color is prohibited.

## Colors

The palette is anchored by a high-contrast foundation of deep blacks and clinical whites, punctuated by a singular vibrant "Electric Blue" for primary actions.

- **`{colors.primary}` (#0070F3)**: Call-to-actions, active states, critical paths, category labels
- **`{colors.on-primary}` (#ffffff)**: Text on primary-colored surfaces
- **`{colors.background}` (#FFFFFF)**: Page background, primary surface
- **`{colors.on-background}` (#111111)**: Primary text, headings, high-emphasis elements
- **`{colors.surface-subtle}` (#F5F5F7)**: Secondary backgrounds, code blocks, subtle UI layering
- **`{colors.border-subtle}` (#EAEAEA)**: Card borders, dividers, structural outlines
- **`{colors.text-muted}` (#666666)**: Secondary text, descriptions, metadata
- **`{colors.success}` (#4ADE80)**: Success states, positive indicators, terminal accents
- **`{colors.warning}` (#FACC15)**: Warning indicators, caution states
- **`{colors.error}` (#F87171)**: Error states, destructive actions

**Design Rationale**: The default mode is **Light**. The high-contrast nature of the tokens allows for a seamless transition to a "Dark" theme where `{colors.on-background}` becomes the primary surface. The single accent color (`{colors.primary}`) prevents chromatic noise — additional hues are reserved exclusively for semantic status indicators (success/warning/error).

## Typography

The typography system leverages **Geist** for its exceptional legibility and modern, geometric proportions. It is supplemented by **Geist Mono** for technical data and labels, reinforcing the functional aesthetic.

### Weight System
- `400` — Body text, descriptions, long-form reading
- `500` — UI labels, navigation, interactive text
- `600` — Section headings, active states, emphasis
- `700` — Hero display only

### Principles
- **Tight tracking on headlines**: Negative letter-spacing (`-0.04em` at 40px) creates a sense of structural permanence and compressed authority. Tracking progressively relaxes as size decreases.
- **Generous line-height for body**: 1.6 line-height ensures readability during prolonged sessions of documentation reading.
- **Monospace for technical identity**: Geist Mono is used for all code, terminal commands, metadata, and technical labels — providing clear visual differentiation from editorial content.
- **No decorative fonts**: The entire typographic system uses two font families only.
- **Uppercase labels**: Geist Mono at 11px with 0.05em tracking for category labels and metadata annotations.

## Layout

This design system utilizes a **Fixed Grid** model for desktop to maintain structural integrity, transitioning to a **Fluid Grid** for mobile devices.

### Grid
- **Columns**: 12-column system with 24px gutters
- **Container max-width**: 1200px, centered with auto margins
- **Edge margins**: 32px on desktop

### Responsive Breakpoints

| Breakpoint | Columns | Margins | Notes |
|------------|---------|---------|-------|
| Desktop (>1024px) | 12 | 32px | Full grid, multi-column layouts |
| Tablet (768–1023px) | 8 | 24px | Collapsing grids |
| Mobile (<767px) | 4 | 16px | Single column, headline scales to 32px |

### Page Structure
```html
<header>          <!-- Sticky top-0, border-bottom, bg-white -->
  <nav>           <!-- max-w-[1200px], mx-auto, px-8 -->
    wordmark | nav links | CTA buttons
  </nav>
</header>
<main>
  <hero>          <!-- Centered, text-center, max-w-2xl -->
    label          <!-- Category — blue, mono, uppercase -->
    headline       <!-- 40px bold, tight tracking -->
    description    <!-- 18px normal, text-muted, generous line-height -->
    CTA group      <!-- flex row: primary + ghost buttons -->
    code block     <!-- Command or install snippet + copy icon -->
  </hero>
  <features>      <!-- Grid sections below the fold -->
</main>
<footer>          <!-- border-t, centered, muted links -->
```

## Elevation & Depth

To maintain a clean, technical feel, depth is communicated through **Tonal Layers** and **Low-Contrast Outlines** rather than heavy shadows.

### Planes
Surfaces are strictly flat. Differentiation between the background and a "card" is achieved by moving from `#FFFFFF` to `#F5F5F7` or by using a 1px solid border (`#EAEAEA`).

### Shadows
When necessary for temporary overlays (modals or dropdowns), use a single, ultra-diffused shadow:
```css
box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.12);
```

### Focus States
Active elements use a 2px offset ring in the primary blue (`{colors.primary}`) to ensure high visibility without altering the element's footprint.

### Anti-Gradient Rule
No gradients. All depth is achieved through contrast and tonal layering. This keeps the interface feeling fast, technical, and honest.

## Shapes

The shape language is disciplined and "Soft-Square." By utilizing a consistent **0.25rem (4px)** corner radius (`{rounded.sm}`), the UI feels modern and approachable without losing its architectural, technical rigor.

| Element | Radius | Notes |
|---------|--------|-------|
| Buttons | `{rounded.sm}` | Avoid pill shapes; maintain grid-aligned geometry |
| Inputs | `{rounded.sm}` | Consistent with buttons |
| Cards | `{rounded.md}` | Larger radius differentiates containers from controls |
| Code blocks | `{rounded.md}` | Matches card radius for visual consistency |
| Chips/Badges | `{rounded.sm}` | Matches button geometry |

## Components

### Navigation (Header)
- **Position**: Sticky top-0, white background
- **Bottom border**: 1px solid `#EAEAEA` (subtle structural line)
- **Content**: Wordmark (bold Geist Sans) | text links | CTA buttons (ghost + primary)
- **Container**: Max 1200px, centered, horizontal padding 32px
- **Link style**: 14px, weight 400, `{colors.on-background}`, no underline. Hover: `{colors.text-muted}`

### Buttons

Buttons adhere to the tokens defined in the frontmatter (`button-primary`, `button-ghost`, `button-danger`).

**Primary**
- Icon: Optional trailing arrow (`→`)
- Hover: slight opacity reduction (90%) or subtle lift
- Active: opacity 85%

**Ghost / Secondary**
- Border: 1px solid `#EAEAEA`
- Icon: Optional leading icon
- Hover: `background: {colors.surface-subtle}`

**Danger**
- Hover: opacity 90%

### Hero Section
- **Label**: Category text — primary blue (`{colors.primary}`), Geist Mono, 11px, uppercase, tracking 0.05em
- **Headline**: 40px, weight 700, -0.04em tracking, centered, `{colors.on-background}`
- **Description**: 18px, weight 400, `{colors.text-muted}`, line-height 1.6, centered, max-width ~600px
- **CTA Group**: Two buttons side-by-side (primary dark + ghost), flex row with gap
- **Code Block**: Command snippet with copy-to-clipboard icon (see Code Block below)

### Code Block
- **Background**: `{colors.surface-subtle}` (ghost-white surface)
- **Border**: 1px solid `{colors.border-subtle}`
- **Radius**: 8px
- **Font**: Geist Mono, 13px, weight 400
- **Text color**: `{colors.on-background}`
- **Prefix**: `$` character in muted gray for shell commands
- **Copy icon**: Positioned right, subtle gray (`{colors.text-muted}`), hover darkens to `{colors.on-background}`

### Terminal UI Component
- **Background**: `#1A1A1A` (deep black)
- **Window chrome**: Three colored dots (red `#F87171`, yellow `#FACC15`, green `#4ADE80`) — macOS-style
- **Font**: Geist Mono, 13px
- **Text**: White on dark background
- **Purpose**: Displays terminal/CLI output in a realistic context

### Cards
- **Background**: `{colors.background}`
- **Border**: 1px solid `{colors.border-subtle}`
- **Radius**: 8px
- **Padding**: 24px
- **Shadow**: None. Depth is conveyed purely through border and tonal shift.
- **Headers**: Slight gray background (`{colors.surface-subtle}`) to separate metadata from content.

### Chips / Badges
- **Font**: Geist Mono (monospace required)
- **Background**: `{colors.surface-subtle}` for neutral status
- **Text**: `{colors.on-background}`
- **Tinted variants**: Subtle colored backgrounds for success (green) or error (red) states

### Input Fields
- **Background**: `{colors.background}`
- **Border**: 1px solid `{colors.border-subtle}`
- **Radius**: 4px
- **Padding**: `8px 12px`
- **Font**: Geist Mono for data entry; Geist Sans for labels
- **Focus**: Border transitions to primary blue (`{colors.primary}`) with a subtle outer glow

### Lists
- Clean rows separated by 1px horizontal lines (`#EAEAEA`)
- High-density layouts preferred: 8px–12px vertical padding per row
- Monospace for technical values within list items

### Footer
- **Top border**: 1px solid `{colors.border-subtle}`
- **Background**: Inherits page background (`{colors.background}`)
- **Padding**: 24px vertical, centered within max-width container
- **Link style**: 12px, weight 400, `{colors.text-muted}`, hover `{colors.on-background}`
- **Layout**: Flex row, space-between, wraps on mobile

## Do's and Don'ts

### Do
- Use `{colors.on-background}` instead of `#000000` for body text (softer on the eyes while maintaining high contrast).
- Use `#000000` for buttons and wordmarks that require maximum visual weight.
- Use 1px solid `{colors.border-subtle}` borders on cards and containers — no shadows for standard elevation.
- Keep negative tracking proportional to size: -0.04em at 40px, -0.02em at 24–32px, normal below 18px.
- Use the weight system: 400 (reading), 500 (UI), 600 (headings), 700 (hero display only).
- Use Geist Mono for all technical content: code, commands, metadata, status labels.
- Keep the palette achromatic except for the single accent blue and semantic status colors.
- Use generous whitespace to establish hierarchy rather than decorative elements.
- Use pure SVG for all icons and graphics to guarantee sharpness on all resolutions and minimize file size.

### Don't
- Don't use gradients, decorative imagery, or illustrations.
- Don't use pill-shaped buttons — maintain the grid-aligned 4px radius.
- Don't use drop shadows on cards — use borders and tonal shifts instead.
- Don't introduce new accent colors beyond `{colors.primary}` without justification.
- Don't use positive letter-spacing on Geist Sans headlines.
- Don't use weight 700 below 32px — it breaks the typographic hierarchy.
- Don't use decorative or semantic colors (success/warning/error) for non-status purposes.
- Don't use more than two font families — Geist Sans and Geist Mono are sufficient.
