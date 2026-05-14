# Design System — David Kaufmann Portfolio

> A living document describing the visual language, component patterns, and interaction design of [kaufmann.dev](https://kaufmann.dev).
> Built with Astro. Styled with vanilla CSS. No frameworks.

---

## 1. Design Philosophy

### 1.1 Core Identity

This is a **personal portfolio** for a Vienna-based developer. The design must communicate:

- **Technical competence** — clean structure, sharp typography, precision in spacing
- **Approachability** — warm language (emojis in copy), generous whitespace, smooth transitions
- **Confidence without arrogance** — no heavy gradients, no neon, no excessive animation

### 1.2 Design Direction

The visual direction sits at the intersection of **minimalist functionalism** and **subtle warmth**:

- **Information architecture first** — content hierarchy drives every decision
- **Grayscale foundation** — black, white, and grays form the base; color is used sparingly as ambient atmosphere
- **Precision in restraint** — every element earns its place; no decorative filler
- **Motion with purpose** — transitions are smooth but never performative

### 1.3 Temperament

| Attribute | Value |
|-----------|-------|
| Density | Medium — breathable but not sparse |
| Temperature | Cool-neutral with warm undertones |
| Personality | Professional, understated, precise |
| Visual weight | Light — high background-to-ink contrast |

---

## 2. Color System

### 2.1 CSS Custom Properties

```css
:root {
    --background: linear-gradient(to bottom, #FAFAFA 0%, transparent 30%, transparent 70%, #FAFAFA 100%),
        radial-gradient(ellipse at 120% 60%, #ff255030 0%, transparent 60%),
        radial-gradient(ellipse at -20% 60%, #55CDFC50 0%, transparent 60%),
        #fafafa;
    --bg-color: #fafafa;
    --text-main: #1a1a1a;
    --text-secondary: #555555;
    --border-color: rgba(0, 0, 0, 0.05);
    --accent-color: #000000;
    --hover-bg: rgba(0, 0, 0, 0.06);
}
```

### 2.2 Palette Breakdown

| Token | Hex / Value | Usage |
|-------|-------------|-------|
| **Background** | `#fafafa` with layered gradients | Page background — warm off-white with subtle pink and blue radial glows at the edges |
| **Text Main** | `#1a1a1a` | Headings, primary text, logo-equivalent name |
| **Text Secondary** | `#555555` | Body text, descriptions, secondary labels |
| **Accent** | `#000000` | Buttons, links, interactive elements, h1 headings |
| **Border** | `rgba(0,0,0,0.05)` | Dividers, card borders, navbar border-bottom |
| **Hover BG** | `rgba(0,0,0,0.06)` | Image placeholders, subtle hover states |

### 2.3 Gradient Atmosphere

The background is a **4-layer stack**:

1. **Base**: `#fafafa` warm off-white
2. **Bottom fade**: Vertical gradient to transparent in the middle, fading back to `#fafafa` at the bottom
3. **Pink glow**: Radial gradient at `120% 60%`, `#ff2550` at 30% opacity — soft sunset warmth
4. **Blue glow**: Radial gradient at `-20% 60%`, `#55CDFC` at 30% opacity — cool counterbalance

> These gradients are extremely subtle and serve as **ambient atmosphere**, not decoration. They prevent the page from feeling sterile without introducing "AI slop" purple gradients.

### 2.4 Selection & Scrollbar

- **Selection**: `background: var(--text-main); color: #fff;` — inverted high contrast
- **Scrollbar**: Thin, `6px` width, `--text-secondary` thumb on `--bg-color` track, rounded

---

## 3. Typography

### 3.1 Font Family

```css
font-family: 'Google Sans Flex', sans-serif;
```

- **Weights used**: 400 (Regular), 500 (Medium), 600 (SemiBold), 700 (Bold)
- **Loaded via**: `@fontsource/google-sans-flex`

### 3.2 Type Scale

| Element | Size | Weight | Line Height | Color |
|---------|------|--------|-------------|-------|
| **H1** | `2.5rem` (40px) | 700 | Default | `--accent-color` (#000) |
| **H2** | `1.5rem` (24px) | 600 | Default | `--text-main` |
| **H3** | `1.125rem` (18px) | 500 | Default | `--text-main` |
| **Body** | `1rem` (16px) | 400 | `1.6` | `--text-secondary` |
| **Nav Links** | `15px` | 500 | Default | `--text-secondary` |
| **Buttons** | `15px` | 500 | Default | `#fff` on `--accent-color` |
| **Tech Tags** | `0.95rem` | 400 | Default | `--text-secondary` |
| **Captions** | `12px` | 400 | Default | `--text-secondary` |

### 3.3 Typography Principles

- **No decorative icons per heading** — the project uses inline SVG icons inside buttons, not as bullet decorators
- **Word break**: `break-word` on H1 for long names; `keep-all` on list items
- **Text wrap**: Natural flow, no forced truncation except image grid detail text (`white-space: nowrap; text-overflow: ellipsis`)

---

## 4. Layout & Spacing

### 4.1 Container System

```
.container          — flex column, centered, flex: 1, padding: 100px 20px 30px
.containerchild     — max-width: 80ch, fadeInUp animation on entry
.box                — margin-top: 20px, content sections
```

- **Max content width**: `80ch` (~640-720px depending on font) — optimal reading measure
- **Page padding**: `20px` horizontal, `100px` top (accounts for fixed navbar), `30px` bottom

### 4.2 Grid Systems

**Image Grid** (`#imgcontainer`):
- Mobile: `repeat(2, 1fr)`
- Tablet (≥640px): `repeat(3, 1fr)`
- Desktop (≥1024px): `repeat(4, 1fr)`
- Gap: `20px`

**Projects Grid** (`.projects-grid`):
- Single column
- Gap: `10px`
- Separators: `5px solid var(--border-color)` between projects, `30px` padding-bottom

**Project Card Row** (`.project-card-row`):
- Desktop: Horizontal flex, `24px` gap, image `250px` fixed width
- Mobile (≤768px): Stacks vertically, image `100%` width

### 4.3 Spacing Tokens

| Token | Value | Usage |
|-------|-------|-------|
| xs | `6px` | Button padding vertical |
| sm | `8px` | Icon gaps, small spacing |
| md | `10px` | List item margins, container gaps |
| lg | `15px` | Section margins, nav link padding |
| xl | `20px` | Grid gaps, avatar margin, section spacing |
| 2xl | `24px` | Project card row gap |
| 3xl | `30px` | Mobile menu gap, project separator padding |
| 4xl | `40px` | Nav pill horizontal padding |
| 5xl | `100px` | Top page padding (navbar offset) |

---

## 5. Components

### 5.1 Navigation (Navbar)

**Desktop**:
- Fixed top, full width, `z-index: 100`
- Background: `rgba(250,250,250,0.8)` with `backdrop-filter: blur(12px)`
- Border-bottom: `1px solid var(--border-color)`
- Shadow: `0 4px 20px -10px rgba(0,0,0,0.05)`
- Links centered, pill-shaped (`border-radius: 40px`), `15px` gap between items
- Link hover: color transitions to `--text-main`
- Active state: `color: var(--text-main); font-weight: 600;`

**Mobile** (≤600px):
- Hamburger button: 2 bars, `24px` wide, `2px` height, animated to X on open
- Full-screen overlay menu: `100vw × 100vh`, centered flex column
- Background: `rgba(250,250,250,0.8)` with `blur(20px)`
- Links: `24px` font, `600` weight, larger touch targets (`15px 30px` padding)
- Entrance: `opacity 0 → 1`, `translateY(-20px) → 0`, `0.4s` ease

**Hamburger Animation**:
```css
/* Open state */
.bar:nth-child(1) { transform: translateY(4px) rotate(45deg); }
.bar:nth-child(2) { transform: translateY(-4px) rotate(-45deg); }
```
Easing: `cubic-bezier(0.175, 0.885, 0.32, 1.275)` — bouncy, organic

### 5.2 Buttons & CTAs

**Primary Button** (`.contact-btn`, `.project-btn`):
- Background: `--accent-color` (#000)
- Text: `#fff`
- Padding: `6px 12px`
- Border-radius: `5px` — **sharp, not rounded** (intentional design choice)
- Hover: background → `--text-secondary` (#555)
- **Shine effect**: Pseudo-element with animated gradient sweep (`highlightSlide`, 3s infinite)

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
- `20px × 20px`
- `fill: currentColor`
- Placed after text with `gap: 8px` (contact) or `10px` (project)

### 5.3 Project Card

```
┌─────────────────────────────────────────┐
│ ┌─────────┐  ┌────────────────────────┐ │
│ │ Image   │  │ Title          [Button]│ │
│ │ (250px) │  │ Category               │ │
│ │         │  │ • Bullet point         │ │
│ └─────────┘  │ • Bullet point         │ │
│              │ [Tag] [Tag] [Tag]       │ │
│              └────────────────────────┘ │
└─────────────────────────────────────────┘
```

- Image: `250px` fixed width desktop, `100%` mobile
- Content area: `flex: 1`, `min-width: 0` (prevents flex overflow)
- Responsive: Stacks vertically below `768px`
- Supports `<picture>` with mobile-specific `srcset`

### 5.4 Tech Tags

```css
.tech-tag {
    background-color: rgba(0, 0, 0, 0.05);
    padding: 3px 7px;
    border-radius: 5px;
    font-size: 0.95rem;
    color: var(--text-secondary);
}
```

- Container: flex wrap, `8px` gap
- Extremely subtle — nearly monochrome

### 5.5 Avatar

- Size: `100px × 100px`
- Shape: **Squircle** via SVG mask
- Hover: `transform: scale(1.05)`
- Transition: `0.3s cubic-bezier(0.4, 0, 0.2, 1)`

### 5.6 Media Containers

**Image Container** (`.img-container`):
- Background: `#00000008` (very subtle dark tint)
- Border-radius: `5px`
- Overflow: hidden
- Image max-width: `500px`, centered with `margin: auto`

**3D Viewer** (`.viewer`):
- Aspect ratio: `4 / 3`
- Max-height: `375px`
- Background: `#00000008`
- Border-radius: `5px`

**Video**:
- Same constraints as images: `max-width: 500px`, centered
- Border-radius: `5px`

---

## 6. Animation & Motion

### 6.1 Entrance Animation

```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
```

- Applied to: `.containerchild`
- Duration: `0.8s`
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)` — Material Design standard ease

### 6.2 Button Shine

```css
@keyframes highlightSlide {
    0%   { left: -150%; }
    50%  { left: 150%; }
    100% { left: -150%; }
}
```

- Duration: `3s`
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)`
- Loop: infinite
- Creates a subtle light sweep across buttons — adds life without distraction

### 6.3 Hover Transitions

| Element | Property | Duration | Easing |
|---------|----------|----------|--------|
| Links (color) | `color` | `0.3s` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Buttons (bg) | `background-color` | `0.3s` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Avatar | `transform` | `0.3s` | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Nav links | `all` | `0.2s` | `ease` |
| Mobile menu | `all` | `0.4s` | `cubic-bezier(0.175, 0.885, 0.32, 1.275)` |

### 6.4 View Transitions

- Powered by Astro's `<ViewTransitions />`
- Native browser API for page transitions
- Custom script handles Cloudflare email decode re-execution on swap

---

## 7. Responsive Breakpoints

| Name | Width | Changes |
|------|-------|---------|
| **Mobile** | ≤600px | Hamburger nav, fullscreen menu, single column projects, 2-col image grid |
| **Tablet** | 640px–1023px | 3-col image grid |
| **Desktop** | ≥1024px | 4-col image grid, horizontal project cards |
| **Project stack** | ≤768px | Project cards stack vertically (image above content) |

---

## 8. Accessibility

- **Focus states**: `outline: 2px solid var(--text-secondary); outline-offset: 2px;` on buttons and links
- **ARIA**: Hamburger button has `aria-label="Toggle navigation"` and `aria-expanded` state
- **Reduced motion**: Not explicitly implemented but single-entrance animations degrade gracefully
- **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<figure>`, `<figcaption>` used correctly
- **Lazy loading**: Project card images use `loading="lazy"`
- **Alt text**: All images have descriptive alt text

---

## 9. Asset Guidelines

### 9.1 Images

| Type | Format | Max Width | Notes |
|------|--------|-----------|-------|
| Project screenshots | WebP | ~570–615px (mobile) / desktop variant | Dual srcset for responsive |
| Article images | WebP | 500px displayed | Often historical/educational photos |
| Portrait | WebP | 100px displayed | Squircle mask applied |
| Favicon | ICO | Standard | Plus `apple-touch-icon.png` |

### 9.2 3D Models

- Format: `.glb` (Binary glTF)
- Viewer: `@google/model-viewer`
- Settings: `camera-controls`, `auto-rotate`, `tone-mapping="neutral"`, `exposure="0.6"`, `field-of-view="30deg"`

### 9.3 Icons

- Source: Inline SVG (Font Awesome paths extracted)
- Size: `20px × 20px`
- Color: `currentColor` — inherits from parent
- Used in: Contact buttons, project CTAs

---

## 10. File Structure

```
src/
├── components/
│   ├── Head.astro          — Meta, viewport, favicon, ViewTransitions
│   ├── Nav.astro           — Fixed navbar with mobile hamburger
│   └── ProjectCard.astro   — Reusable project card component
├── layouts/
│   └── Layout.astro        — Root layout: Head + Nav + Container + Slot
├── pages/
│   ├── index.astro         — Homepage: Avatar, name, bio, contact links
│   ├── projects.astro      — Projects grid with ProjectCard instances
│   └── article/
│       └── ct2mesh2print.astro  — Long-form article with 3D viewer
└── styles/
    └── global.css          — All styles: tokens, components, utilities, animations
```

---

## 11. Design Decisions Log

| Decision | Rationale |
|----------|-----------|
| **Sharp corners (5px)** instead of heavy rounding | Communicates precision and technical focus; avoids the "rounded card slop" look |
| **Grayscale base with subtle gradients** | Keeps focus on content and project imagery; gradients are atmospheric, not decorative |
| **Google Sans Flex** | Modern, geometric sans with excellent legibility; "Flex" variant offers optical size axis |
| **No decorative icons on headings** | Content speaks for itself; avoids visual noise |
| **Button shine animation** | Adds subtle life to CTAs without being flashy; references polished product design |
| **80ch max width** | Optimal reading measure for body text; prevents line lengths that strain reading |
| **Single global CSS file** | For a site of this scale, one file is simpler than a CSS-in-JS or utility system; Astro scopes page styles when needed |
| **No dark mode** | The warm off-white and subtle gradients are integral to the identity; dark mode would require a complete rethinking of the atmospheric background |
| **Pill nav links** | Softens the navigation while keeping content areas sharp; creates a clear "active" state container |
| **Squircle avatar** | Friendlier than a perfect circle, more distinctive than a rounded rectangle; references modern app icon design |

---

## 12. Anti-Patterns (What We Avoid)

| Pattern | Why Avoided |
|---------|-------------|
| Purple/blue gradient hero backgrounds | AI slop — generic, overused, dilutes personal brand |
| Emoji as bullet icons | Looks unprofessional for a developer portfolio |
| Heavy drop shadows on cards | Would add visual weight counter to the light aesthetic |
| Rounded cards with left accent borders | Tailwind/component-library cliché |
| Decorative stats/quotes sections | No filler content — every element earns its place |
| Multi-color tag system | Would introduce unnecessary chromatic noise; monochrome tags keep focus on content |

---

## 13. Future Considerations

- **Dark mode**: Would require rethinking the gradient background entirely; not a simple inversion
- **Blog index**: Article pages exist but no listing page; could add `/articles` with the same card pattern
- **Image optimization**: Currently manual WebP; could integrate Astro's image optimization
- **i18n**: Site is English-only; German variant possible given Vienna base
- **RSS**: Long-form articles would benefit from RSS feed

---

> *Last updated: 2026-05-14*
> *Maintained alongside the codebase — update this document when design tokens or patterns change.*
