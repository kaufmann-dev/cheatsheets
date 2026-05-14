# Purus CSS — Design Document

> **Minimalist CSS Framework**
> 
> No JavaScript. Raw CSS.

## Design Philosophy

Purus CSS is built on a single conviction: **the web needs less, not more**. In an era of 200KB CSS-in-JS bundles and JavaScript-dependent styling, Purus CSS returns to fundamentals. It provides a complete, usable design system in a single 14.3KB minified file — no build steps, no runtime, no dependencies.

### Core Principles

1. **Zero JavaScript**: Styling is a presentational concern. Purus CSS does not use JavaScript for any visual behavior. This eliminates hydration mismatches, reduces attack surface, and ensures styles work even when scripts fail or are disabled.

2. **Raw CSS**: No preprocessor lock-in, no custom syntax, no compilation required. Write CSS that runs in every browser exactly as authored. This is a deliberate constraint that maximizes portability and longevity.

3. **Customization via CSS Variables**: The entire visual system is exposed through CSS custom properties. Change one variable in a custom stylesheet loaded after Purus, and the entire framework adapts. No Sass variables, no build-time theming.

4. **Normalization over Reset**: Built alongside [modern-normalize](https://github.com/sindresorhus/modern-normalize), Purus CSS normalizes cross-browser inconsistencies rather than obliterating defaults. This preserves semantic HTML behavior while ensuring predictability.

5. **Utility Classes as Augmentation**: Purus CSS provides utility classes for common needs, but the core value is in the drop-in base styles. Utilities are helpers, not the primary interface.

## Visual Language

### Color System

The color palette is intentionally restrained — one primary action color, a neutral grayscale, and an error state. This is not a limitation; it is a guardrail against visual noise.

| Token | Default Value | Role |
|-------|---------------|------|
| `--grey-border` | `#d1d1d1` | Structural dividers, table borders, input borders |
| `--grey-text` | `#7d7d7d` | Secondary text, muted captions, blockquotes |
| `--white` | `#ffffff` | Primary background |
| `--white-darker` | `#f9f9f9` | Alternate backgrounds (tables, footer, code blocks) |
| `--white-darkest` | `#f3f3f3` | Deepest neutral surface (footer background, code blocks) |
| `--black` | `#000000` | Primary text, headings |
| `--primary` | `#4285f4` | Primary action, links, buttons, focus states |
| `--primary-faded` | `#5c95f4` | Hover transitions, disabled button backgrounds |
| `--primary-darker` | `#3c78dc` | Button hover, active navigation states |
| `--primary-darkest` | `#2766cf` | Button active/pressed states |
| `--primary-outline` | `rgba(0, 123, 255, .35)` | Focus rings (box-shadow) |
| `--error` | `#f43022` | Invalid form states, error messages |

**Design Rationale**: The primary blue (`#4285f4`) was chosen for its high contrast against white (WCAG AA compliant), its familiarity across operating systems, and its neutrality — it does not carry the aggressive connotations of red, the transactional connotations of green, or the playful connotations of orange. It is a safe default that can be overridden for brand-specific applications.

### Typography

**Font Stack**: `system-ui, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji'`

This stack prioritizes system fonts, ensuring text renders in the user's native typeface with zero download overhead. It is a performance decision as much as an aesthetic one.

**Base Settings**:
- Font size: `16px` (browser default, respects user preferences)
- Line height: `1.5`
- Tab size: `4`

**Heading Scale**:
- `h1`: `2em` (32px at base)
- `h2`–`h6`: Browser defaults (cascading down from ~1.5em to ~0.67em)

**Code/Monospace**: `ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace`

Preformatted blocks use a subtle background (`var(--white-darkest)`) with a `1px solid var(--grey-border)` border and `3px` border radius. Inline code receives hair-space padding (`\00a0` before/after) to create breathing room without affecting layout.

### Spacing System

Purus CSS uses a two-tier spacing scale:

| Token | Value | Usage |
|-------|-------|-------|
| `--padding` / `--margin` | `5px` | Tight internal spacing, button padding, component gaps |
| `--padding-lg` / `--margin-lg` | `10px` | Section spacing, container padding, navigation padding |

**Container**:
- Max width: `768px` (readable line length for body text)
- Horizontal padding: `16px`
- Centered with `margin: 0 auto`

The small scale (5px / 10px) is intentional. Purus CSS targets content-heavy sites where generous whitespace should be authored intentionally, not enforced by the framework.

### Border Radius

A restrained scale from `0px` to `9999px` (full), with the framework defaulting to `4px` for interactive elements (buttons, inputs) and `3px` for code blocks. No aggressive rounding — corners should not compete with content for attention.

### Shadows

Seven shadow levels (`shadow-sm` through `shadow-2xl` plus `shadow-inner`) using layered, low-opacity black shadows. The default elevation system avoids colored shadows (no blue/purple tints) to maintain neutrality.

## Component Design

### Buttons

```
Background: var(--primary)
Text: var(--white)
Border radius: 4px
Padding: 8px 16px
Font: inherit, 1rem, weight 400
Transition: color, background-color, border-color, box-shadow (150ms ease-in-out)

States:
  Hover:   var(--primary-darker)
  Active:  var(--primary-darkest)
  Focus:   0 0 0 .2rem var(--primary-outline)
  Disabled: opacity .65, cursor not-allowed, background var(--primary-faded)
```

Buttons are flat — no gradients, no borders, no text shadows. The visual hierarchy is established purely through color value and whitespace.

### Form Inputs

```
Background: var(--white-darker)
Border: 1px solid rgba(0, 0, 0, .12)
Border radius: 4px
Padding: 8px 16px
Width: 100% (block-level)
Transition: border-color, box-shadow (150ms ease-in-out)

Focus: border-color var(--primary-faded), box-shadow 0 0 0 .2rem var(--primary-outline)
Invalid: border-color var(--error), color var(--error)
Disabled: background rgba(0,0,0,.12), color rgba(0,0,0,.54)
```

All text inputs, selects, and textareas share identical geometry. This creates visual rhythm in forms — every field occupies the same horizontal space and receives the same focus treatment.

### Tables

```
Border collapse: collapse
Border: 1px solid var(--grey-border)
Cell padding: 1rem
Striping: tr:nth-child(2n) background var(--white-darkest)
Background: var(--white-darker)
```

Tables are bordered and striped by default. There is no hover state on rows — tables in Purus CSS are for data presentation, not interaction.

### Blockquotes

```
Left border: 4px solid var(--grey-border)
Color: var(--grey-text)
Padding: 0 1rem
Margin: 0 0 1rem
```

Blockquotes receive only a left border and muted color. No background, no italic styling, no quotation marks. The visual treatment is structural, not decorative.

### Navigation

Navigation lists are unstyled by default (`padding: 0`, `list-style-type: none`). Horizontal navigation is achieved by placing list items and anchors inline. There is no prescribed navigation pattern — Purus CSS removes default browser styling and lets the author compose navigation as needed.

The footer receives a top border (`var(--grey-border)`) and a `var(--white-darkest)` background, with centered text and `flex-shrink: 0` to remain anchored at the bottom of flex layouts.

## Architecture

### File Organization

| File | Purpose |
|------|---------|
| `purus.css` | Complete framework (classes + drop-in styles) |
| `purus.min.css` | Minified complete framework |
| `purus.drop-in.css` | Base styles only (no utility classes) |
| `purus.drop-in.min.css` | Minified base styles |
| `purus.classes.css` | Utility classes only (no base styles) |
| `purus.classes.min.css` | Minified utility classes |

**Use `purus.css`** for new projects that want the full experience.
**Use `purus.drop-in.css`** when you need the normalization and base styles but plan to write your own layout system.
**Use `purus.classes.css`** when you already have a CSS reset/normalize and only need the utility layer.

### CSS Variable Override Pattern

```css
/* Load Purus CSS first */
<link rel="stylesheet" href="purus.min.css">

/* Then override variables */
<style>
  :root {
    --primary: #d73a49;        /* Your brand red */
    --primary-darker: #cb2431;
    --primary-darkest: #b31d28;
    --grey-border: #e1e4e8;
    --grey-text: #586069;
  }
</style>
```

Because Purus CSS uses CSS custom properties for all themable values, the entire framework can be rebranded without modifying the source file or increasing specificity.

## Design Constraints & Anti-Patterns

### What Purus CSS Does NOT Include

To maintain its minimal footprint and zero-dependency promise, Purus CSS intentionally omits:

- **Grid system**: Use CSS Grid or Flexbox directly. Purus CSS provides `.d-grid` and `.d-flex` utilities but no 12-column abstraction.
- **Component library**: No cards, modals, dropdowns, or carousels. These are application-specific and bloat the framework.
- **Animation utilities**: No `.fade-in`, `.slide-up`, or transition utilities. CSS transitions on interactive elements (buttons, inputs) are baked in, but motion design is left to the author.
- **Dark mode**: No `prefers-color-scheme` media queries. Dark mode is trivial to implement via CSS variable overrides if needed.
- **Print styles**: No `@media print` optimizations. Most Purus CSS sites print reasonably well by default.

### Anti-Patterns to Avoid When Extending

1. **Do not add JavaScript-dependent classes**: Purus CSS works without JS. Adding `.dropdown-open` or `.tab-active` that require script manipulation breaks this contract.

2. **Do not increase specificity**: The framework avoids IDs and `!important`. Keep overrides in the same specificity layer (element/class) to prevent escalation wars.

3. **Do not add decorative utilities**: Purus CSS is not Tailwind. Adding `.bg-gradient-purple` or `.text-shadow-glow` introduces visual noise that conflicts with the framework's neutral philosophy.

4. **Do not shrink the base font size**: The `16px` base is a user-accessibility feature. Reducing it to `14px` or `62.5%` breaks the user's browser preferences.

## Accessibility

- **Focus states**: All interactive elements have visible focus rings using `box-shadow: 0 0 0 .2rem var(--primary-outline)`. Never remove these.
- **Color contrast**: The default primary blue (`#4285f4` on `#ffffff`) meets WCAG 2.1 AA for large text and UI components. If you change the primary color, verify contrast ratios.
- **Form labels**: The framework styles `label` with `display: inline-block` and `line-height: 2` to ensure adequate touch targets and readability. Always associate labels with inputs via `for` attributes.
- **Disabled states**: Disabled buttons and inputs receive `cursor: not-allowed` and visual opacity reduction. Do not rely on color alone to indicate disabled state.

## Browser Support

Purus CSS targets all modern browsers that support CSS custom properties (Chrome 49+, Firefox 31+, Safari 9.1+, Edge 15+). The use of `system-ui` in the font stack and `-webkit-appearance` for form elements follows progressive enhancement — older browsers fall back to the next font in the stack or default form rendering.

## Contributing Design Changes

When proposing visual changes to Purus CSS:

1. Verify the change reduces complexity or solves a common problem, not a niche edge case.
2. Ensure the change does not increase the minified size disproportionately to its value.
3. Prefer CSS variable additions over hardcoded values.
4. Test against the demo page (`website/demo/index.html`) to ensure no regressions in typography, forms, tables, or navigation.
5. Maintain the zero-JavaScript constraint.

---

*Purus CSS is a design system built on restraint. Every line of CSS must justify its existence. When in doubt, remove.*
