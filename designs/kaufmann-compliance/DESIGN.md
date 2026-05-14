# Kaufmann Compliance — Design System

> Domain: Legal document hub (Imprint & Privacy Policy)
> Live URL: legal.kaufmann.dev
> Tech: SvelteKit + Tailwind CSS v4 + Geist font family

---

## 1. Design Philosophy

Kaufmann Compliance is a **functional legal document hub** — not a marketing site. Its design inherits the typographic DNA of Vercel's Geist system (aggressive negative tracking, shadow-as-border, monochrome restraint), but strips away everything that doesn't serve its core job: presenting legal text with clarity and administering document variants across sites.

The visual personality is **bureaucratic precision made beautiful**. Every element exists to serve readability or administrative efficiency. There are no decorative gradients, no hero illustrations, no trust bars. The design's confidence comes from restraint, not ornament.

---

## 2. Core Assets

### Brand Mark
- **File**: `src/lib/assets/favicon.svg`
- **Asset**: Material Design "shield" icon (SVG path)
- **Behavior**: Auto-adapts fill between `#000000` (light mode) and `#ffffff` (dark mode) via `prefers-color-scheme`
- **Usage**: Browser favicon only. No logo mark appears in the UI chrome — the product is entirely typographic.
- **Note**: There is no raster logo, wordmark, or brand imagery. Visual identity is established through typography and spacing alone.

### Font Family
- **Primary**: Geist Sans (variable, woff2, weights 100–900)
- **Monospace**: Geist Mono (variable, woff2, weights 100–900)
- **Path**: `/static/fonts/`
- **OpenType**: `"liga" 1` enabled globally
- **Fallback stack**: `Arial, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol` (sans); `ui-monospace, SFMono-Regular, Roboto Mono, Menlo, Monaco, Liberation Mono, DejaVu Sans Mono, Courier New` (mono)

### Color Tokens (Tailwind v4 `@theme`)

| Token | Value | Actual Usage in Code |
|-------|-------|---------------------|
| `vercel-black` | `#171717` | Primary text, headings, dark buttons, header title, tab active state |
| `vercel-white` | `#ffffff` | Page background, card surfaces, button text on dark |
| `gray-900` | `#171717` | Alias for vercel-black |
| `gray-600` | `#4d4d4d` | Body/description text |
| `gray-500` | `#666666` | Domain text, secondary metadata |
| `gray-400` | `#808080` | Placeholder/empty-state text |
| `gray-100` | `#ebebeb` | Borders, card outlines, dividers |
| `gray-50` | `#fafafa` | Subtle surface tint, inner card highlight, empty-state backgrounds |
| `link-blue` | `#0072f5` | **Not used in any component** (defined but unused) |
| `focus-blue` | `hsla(212, 100%, 48%, 1)` | **Not used in any component** (defined but unused) |
| `badge-blue-bg` | `#ebf5ff` | **Not used in any component** |
| `badge-blue-text` | `#0068d6` | **Not used in any component** |
| `ship-red` | `#ff5b4f` | Delete buttons, revoke buttons, form error text |
| `preview-pink` | `#de1d8d` | **Defined but unused** |
| `develop-blue` | `#0a72ef` | **Defined but unused** |

**Hardcoded colors found in components but NOT in theme**:
- `#eaeaea` — Footer top border (`Footer.svelte`)
- `#888888` — Footer link default color (`Footer.svelte`)
- Tailwind `green-50/200/600/900` — API key success alert only (`admin/+page.svelte`)

---

## 3. Typography Hierarchy (As Actually Implemented)

### Weight System
- `400` — Body text, descriptions, reading
- `500` — UI labels, navigation, emphasized text, select options
- `600` — Headings, active states, card titles, button text
- **No 700 bold anywhere in the codebase**

### Size & Tracking Scale

| Role | Size | Weight | Line Height | Letter Spacing | Used In |
|------|------|--------|-------------|----------------|---------|
| Hero Display | 48px | 600 | 1.00 (tight) | -2.4px | Landing page headline |
| Page Title | 40px | 600 | 1.20 | -2.4px | Imprint/Privacy page headings |
| Section Heading | 32px | 600 | tight | -1.28px | Admin login heading |
| Card Title | 24px | 600 | — | -0.96px | Admin panel card titles, dashboard heading (mobile) |
| Subsection Title | 20px | 600 | — | normal | Site name in admin cards |
| Body Large | 20px | 400 | 1.80 | normal | Landing page description |
| Body | 18px | 400 | — | normal | Imprint field values, privacy prose |
| UI Standard | 16px | 400–600 | — | normal | Form labels, checkbox labels, empty state messages |
| Button / Nav | 14px | 500 | — | normal | Buttons, tabs, inputs, form labels |
| Caption | 12px | 500 | — | normal | Metadata, tag text, API key dates, copy buttons |
| Micro | 11px | 400 | — | normal | Footer links (mobile) |
| Mono Code | 14px | 400 | — | normal | API key display |
| Mono Badge | 12px | 500 | — | normal | API key preview badges |

### Principles
- **Negative tracking is the signature**: -2.4px at 48px/40px creates compressed urgency. Progressively relaxes: -1.28px at 32px, -0.96px at 24px, normal below 20px.
- **Uppercase labels**: 14px medium uppercase with normal tracking for field labels (Name, Address, Email, Editorial Policy).
- **Monospace for technical identity**: Geist Mono used exclusively for API key values and key preview badges — connecting the admin UI to its "developer tool" nature.

---

## 4. Layout Architecture

### Container
- **Max width**: 1200px (`max-w-[1200px]`)
- **Horizontal padding**: 24px (`px-6`)
- **Alignment**: Centered with `mx-auto`

### Page Structure
```
<div class="flex min-h-screen flex-col">
  <Header />          <!-- sticky top-0, shadow-border bottom -->
  <main>              <!-- flex-1, max-w-[1200px], px-6, py-16 -->
    {page content}
  </main>
  <Footer />          <!-- mt-auto, border-t -->
</div>
```

### Spacing
- No rigid 8px grid system is enforced.
- Common values observed: `4px`, `6px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px`, `48px`, `64px`.
- Section gaps in admin: `space-y-8` (32px)
- Card internal padding: `24px` (`p-6`)
- Landing page: `gap-10` (40px) between headline and description

---

## 5. Depth & Elevation (As Actually Used)

The project uses **four distinct shadow patterns**, not a single unified system:

### Pattern A: Header Border
```css
box-shadow: rgba(0,0,0,0.08) 0px 0px 0px 1px;
```
- Used on: `Header.svelte` (sticky header bottom border)
- Purpose: Replaces `border-bottom`

### Pattern B: Input Ring
```css
box-shadow: rgb(235, 235, 235) 0px 0px 0px 1px;
```
- Used on: All text inputs, select dropdowns, language selector
- Purpose: Subtle gray ring for form fields
- Note: Lighter than Pattern A (`#ebebeb` vs `rgba(0,0,0,0.08)`)

### Pattern C: Standard Card
```css
box-shadow: rgba(0,0,0,0.08) 0px 0px 0px 1px,
            rgba(0,0,0,0.04) 0px 2px 2px,
            #fafafa 0px 0px 0px 1px;
```
- Used on: Admin "Add Site" card, Global Defaults cards, "Add API Key" card
- Purpose: Card with border + subtle lift + inner highlight

### Pattern D: Featured Card (Full Stack)
```css
box-shadow: rgba(0,0,0,0.08) 0px 0px 0px 1px,
            rgba(0,0,0,0.04) 0px 2px 2px,
            rgba(0,0,0,0.04) 0px 8px 8px -8px,
            #fafafa 0px 0px 0px 1px;
```
- Used on: Site cards in admin (the most prominent data containers)
- Purpose: Maximum depth for primary content cards

### No Elevation
- Flat white backgrounds for: imprint field groups, empty states, success alerts
- No shadow on: Footer, main content area, prose text

---

## 6. Components (As Actually Implemented)

### Header
- **Position**: `sticky top-0 z-50`
- **Background**: `#ffffff`
- **Bottom border**: Pattern A shadow
- **Height**: Auto (py-4 = 16px vertical padding)
- **Content**: Site name or "Kaufmann Compliance" as 18px semibold link
- **Max width**: 1200px, centered, px-6
- **Behavior**: Links back to origin site (if `siteDomain` provided) or root `/`

### Footer
- **Top border**: `1px solid #eaeaea` (hardcoded, NOT from theme)
- **Background**: Inherits white page background
- **Height**: Auto (py-6 to py-8 responsive)
- **Content**: Three legal links (Imprint, Privacy, Admin) + LanguageSelector
- **Link style**: 11px–12px normal weight, `#888888` default, `#171717` on hover
- **Layout**: Flex row, `justify-between`, wraps on mobile

### Tabs (Admin Navigation)
- **Shape**: `rounded-full` pill buttons
- **Active state**: `bg-[#171717]`, `border-[#171717]`, `text-white`
- **Inactive state**: `bg-white`, `border-[#ebebeb]`, `text-[#171717]`
- **Padding**: `px-5 py-2`
- **Font**: 14px weight 500
- **Container**: `flex gap-2`, `overflow-x-auto`, `no-scrollbar`

### Buttons (Three Variants)

**Primary Dark**
- Background: `#171717`
- Text: `#ffffff`
- Radius: `6px` (`rounded-md`)
- Padding: `px-4 py-2`
- Font: 14px weight 500
- Hover: `opacity-90`
- Used for: Submit, Save, Sign In

**Ghost / Secondary**
- Background: `#ffffff`
- Text: `#171717`
- Radius: `6px`
- Padding: `px-3 py-1.5` to `px-4 py-2`
- Shadow: Pattern B (input ring)
- Hover: `bg-gray-50`
- Font: 12px–14px weight 500
- Used for: Copy URL, Sign Out, secondary actions

**Danger**
- Background: `#ff5b4f` (ship-red)
- Text: `#ffffff`
- Radius: `6px`
- Padding: `px-3 py-1.5`
- Font: 12px weight 500
- Hover: `opacity-90`
- Used for: Delete site, Revoke API key

### Inputs
- **Style**: No traditional CSS border
- **Ring**: Pattern B (`rgb(235,235,235) 0px 0px 0px 1px`)
- **Radius**: `6px`
- **Padding**: `px-3 py-2`
- **Font**: 16px for main inputs, 14px for compact fields
- **Background**: `#ffffff`
- **Focus**: No custom focus style defined (relies on browser default)

### Cards
- **Background**: `#ffffff`
- **Radius**: `8px` (`rounded-lg`)
- **Padding**: `24px` (`p-6`)
- **Shadow**: Pattern C or D depending on prominence
- **No border**: All card edges defined by shadow only

### Language Selector
- **Type**: Native `<select>` with custom chevron SVG
- **Ring**: Pattern B
- **Radius**: `6px`
- **Font**: 14px weight 500
- **Background**: `#ffffff`
- **Chevron**: Custom SVG down-arrow, `text-gray-500`, absolutely positioned

### Success Alert (API Key)
- **Background**: `green-50`
- **Border**: `green-200`
- **Title**: `green-900`, 16px semibold
- **Body**: `green-800`, 14px normal
- **Code block**: White bg, `green-200` border, mono 14px
- **Copy button**: `green-600` bg, white text
- **Note**: This is the **only** use of green in the entire UI. The green palette is not defined in the custom theme and relies on Tailwind's default green scale.

---

## 7. Page-Level Patterns

### Landing Page (`/`)
- **Layout**: Single column, centered, `items-center justify-center`
- **Hero**: 48px semibold, -2.4px tracking, max-width 3xl
- **Description**: 20px normal, `text-gray-600`, max-width xl, line-height 1.80
- **Spacing**: `gap-10` between headline and description
- **Vertical padding**: Inherits `py-16` from main

### Imprint Page (`/imprint`)
- **Max width**: 768px (`max-w-3xl`)
- **Title**: 40px semibold, -2.4px tracking, margin-bottom 48px
- **Field groups**: `space-y-8` (32px)
- **Labels**: 14px medium, uppercase, `text-gray-500`, margin-bottom 8px
- **Values**: 18px normal, `#171717`
- **No cards**: Content sits directly on white background

### Privacy Page (`/privacy`)
- Renders Markdown via `marked` into styled `.prose`
- No custom prose styling observed in codebase — relies on Tailwind's default or browser defaults

### Admin Dashboard (`/admin`)
- **Login state**: Centered form, max-width `sm` (384px), py-20
- **Authenticated state**: Full-width content within 1200px container
- **Card hierarchy**: Add forms → Site list → Global defaults → API keys
- **Site cards**: Full Pattern D shadow, containing nested forms, toggles, and conditional field visibility
- **Grid**: Admin cards use single column; ImprintForm uses `grid-cols-1 md:grid-cols-2` for bilingual inputs

---

## 8. Responsive Behavior

| Breakpoint | Changes Observed |
|------------|-----------------|
| `< 640px` (default) | Single column everywhere. Admin heading drops to 24px. Footer links at 11px. Language selector scaled to 90%. |
| `≥ 640px` (`sm:`) | Footer py-8, links 12px. Language selector at 100%. |
| `≥ 768px` (`md:`) | ImprintForm switches to 2-column grid for bilingual inputs. |
| `≥ 1024px` (`lg:`) | Admin dashboard heading returns to 32px. Site card actions move to `flex-row justify-between`. |

### Touch Targets
- Buttons: Minimum 32px height (py-2 = 8px + line-height ~16px)
- Tab pills: px-5 py-2 (comfortable horizontal padding)
- Footer links: Small text but wrapped in generous container padding

---

## 9. Inconsistencies & Technical Debt

These are honest notes for maintaining design consistency:

1. **Footer border color mismatch**: Footer uses `#eaeaea` while the theme defines `gray-100` as `#ebebeb`. The difference is imperceptible but creates two "nearly identical" border tokens.

2. **Footer link color not in theme**: Footer links use `#888888`, which sits between theme `gray-500` (`#666666`) and `gray-400` (`#808080`). It has no named token.

3. **Unused theme tokens**: `link-blue`, `focus-blue`, `badge-blue-bg`, `badge-blue-text`, `preview-pink`, `develop-blue` are all defined in the Tailwind v4 theme but **never referenced** in any component. They are vestigial from the Vercel design system copy-paste.

4. **Success alert uses default Tailwind green**: The API key success state (`green-50`, `green-200`, `green-600`, `green-900`) is the only chromatic color in the entire UI and is not part of the custom theme.

5. **Focus states are undefined**: No custom `:focus` or `:focus-visible` styles exist. Interactive elements rely on browser defaults, which means focus rings will be inconsistent across browsers.

6. **Two checkbox styles**: Admin site toggles use unstyled native checkboxes (`h-4 w-4`), while form checkboxes in other contexts are not used — creating an isolated checkbox pattern.

7. **No disabled state styling**: Buttons and inputs have no explicit disabled visual treatment.

---

## 10. Agent Prompt Guide

### Quick Reference
- **Primary text**: `#171717` (not pure black)
- **Background**: `#ffffff`
- **Body text**: `#4d4d4d` (gray-600)
- **Muted text**: `#666666` (gray-500)
- **Border/subtle**: `#ebebeb` (gray-100) or `rgb(235,235,235)` for input rings
- **Danger/action negative**: `#ff5b4f` (ship-red)
- **Card shadow**: Pattern C or D (see Section 5)
- **Input shadow**: `rgb(235, 235, 235) 0px 0px 0px 1px`

### Component Patterns

**Header**
```
Sticky top-0 z-50 bg-white. Bottom shadow: rgba(0,0,0,0.08) 0px 0px 0px 1px.
Content: mx-auto max-w-[1200px] px-6 py-4.
Title: 18px Geist weight 600, #171717, no underline.
```

**Footer**
```
Border-t border-[#eaeaea]. mx-auto max-w-[1200px] px-6 py-6 sm:py-8.
Links: 11px–12px normal weight, #888888 default, hover:text-[#171717].
Layout: flex-row justify-between, gap-2.
```

**Card (Standard)**
```
Rounded-lg (8px), bg-white, p-6.
Shadow: rgba(0,0,0,0.08) 0px 0px 0px 1px, rgba(0,0,0,0.04) 0px 2px 2px, #fafafa 0px 0px 0px 1px.
```

**Card (Featured / Site Card)**
```
Same as standard PLUS: rgba(0,0,0,0.04) 0px 8px 8px -8px
```

**Input**
```
No CSS border. Shadow: rgb(235,235,235) 0px 0px 0px 1px.
Rounded-md (6px), px-3 py-2, 16px Geist weight 400, #171717.
```

**Primary Button**
```
Rounded-md (6px), bg-[#171717], text-white, px-4 py-2.
Font: 14px Geist weight 500. Hover: opacity-90.
```

**Ghost Button**
```
Rounded-md (6px), bg-white, text-[#171717], shadow-input-ring.
Hover: bg-gray-50. Font: 12px–14px weight 500.
```

**Danger Button**
```
Rounded-md (6px), bg-[#ff5b4f], text-white, px-3 py-1.5.
Font: 12px weight 500. Hover: opacity-90.
```

**Tab Pill**
```
Rounded-full, px-5 py-2, 14px weight 500.
Active: bg-[#171717] + border-[#171717] + text-white.
Inactive: bg-white + border-[#ebebeb] + text-[#171717].
```

**Field Label**
```
14px Geist weight 500, uppercase, tracking-normal, text-gray-500.
Margin-bottom: 8px.
```

**Hero Display**
```
48px Geist weight 600, line-height 1.00, tracking -2.4px, #171717.
```

---

## 11. Do's and Don'ts

### Do
- Use `#171717` instead of `#000000` for all primary text
- Use shadow-as-border for inputs (`rgb(235,235,235)`) and cards (`rgba` stack)
- Keep negative tracking proportional to size: -2.4px at 48px, -1.28px at 32px, -0.96px at 24px
- Use the three-weight system: 400 (read), 500 (UI), 600 (headings)
- Use uppercase 14px medium for field labels
- Use Geist Mono exclusively for API keys and technical metadata
- Keep the palette achromatic except for ship-red on destructive actions

### Don't
- Don't use the unused theme tokens (`link-blue`, `preview-pink`, `develop-blue`, `focus-blue`) — they have no established UI pattern
- Don't use traditional CSS `border` on cards — maintain the shadow-border convention
- Don't use weight 700 anywhere
- Don't add decorative imagery, gradients, or illustrations — this is a legal tool, not a marketing site
- Don't use positive letter-spacing on Geist Sans
- Don't introduce new colors without updating this document — the current palette is intentionally minimal

---

*Document based on actual source code audit. Last updated: 2026-05-14.*
