# MarketDeck — Design System

> **Project type:** Data-dense financial dashboard (local web app)
> **Primary viewport:** 13–27" desktop monitor, 1–2m viewing distance
> **Secondary viewport:** Mobile phone (quick checks, not primary analysis)
> **Visual temperature:** Cold, authoritative, terminal-like
> **Narrative role:** This is a tool, not a story. Every pixel serves data legibility.

---

## 1. Design Philosophy

### 1.1 Direction

MarketDeck is designed as a **professional trading terminal** that happens to run in a browser. The aesthetic borrows from:

- **Bloomberg Terminal** — information density, monochrome data, zero decorative chrome
- **Dieter Rams / Braun** — "less but better"; every element earns its place
- **Swiss International Style** — grid discipline, asymmetric balance, uppercase micro-labels

The emotional register is **cold authority**. Users come here to make decisions with money. Warmth, playfulness, or "delight" would undermine trust.

### 1.2 Core Principles

| # | Principle | Application |
|---|---|---|
| 1 | **Data first, chrome never** | No decorative illustrations, no gradient backgrounds on cards, no shadows for elevation |
| 2 | **Zero radius, zero sentiment** | Every interactive element is a rectangle. No rounded corners — they signal "friendly consumer app" |
| 3 | **Monochrome discipline** | No green/red for up/down. White = positive, grey = negative. Color is reserved for user-defined tag badges only |
| 4 | **Density is a feature** | 50+ data points visible without scrolling on a 1080p screen |
| 5 | **Motion is information** | Animations only for state changes (loading, transitions), never for decoration |

### 1.3 What We Deliberately Avoid (Anti-Patterns)

| Pattern | Why We Avoid It |
|---|---|
| Rounded corners (cards, buttons, tags) | Signals "friendly SaaS"; contradicts terminal authority |
| Green/red for returns | Too emotional; monochrome forces users to read numbers, not react to color |
| Hero illustrations / empty-state graphics | No empty states exist; the app is functional from first load |
| Gradient backgrounds | The subtle radial gradients on `body` are the *only* exception, and they are nearly imperceptible |
| Emoji in UI | Replaced with geometric symbols (`+`, `✕`, `✎`, `●`, `○`) |
| Decorative icons next to every label | Labels are uppercase with letter-spacing; icons would add noise |

---

## 2. Color System

### 2.1 Core Palette

| Token | Value | Usage |
|---|---|---|
| `--bg-base` | `#000000` | Page background |
| `--bg-surface` | `rgba(255,255,255,0.05)` | Sidebar, cards, banners, status bar |
| `--bg-surface-elevated` | `rgba(255,255,255,0.07)` | Hover states, active sidebar item |
| `--bg-surface-hover` | `rgba(255,255,255,0.09)` | Button hovers |
| `--border-subtle` | `#222222` | Dividers, table borders, inactive button borders |
| `--border-strong` | `#333333` | Input borders, card borders |
| `--border-hover` | `#555555` | Hover borders |
| `--text-primary` | `#ffffff` | Headlines, active controls, positive returns, primary actions |
| `--text-secondary` | `#a0a0a0` | Body text, descriptions, inactive nav items |
| `--text-tertiary` | `#666666` | Labels, timestamps, metadata, negative returns |

### 2.2 Functional Accents

| Token | Value | Usage |
|---|---|---|
| `--accent-positive` | `#ffffff` | Positive returns, buy signals, rank badges (top N) |
| `--accent-negative` | `#777777` | Negative returns, skip signals, failed states |

> **Note:** We intentionally do NOT use green/red. The app is designed for users who look at returns all day — chromatic fatigue is real. White/grey differentiation is calmer and forces numeric reading.

### 2.3 User-Defined Color (Tags Only)

Tag colors are the **only** place user-defined color appears. The system auto-generates a subtle treatment from a single hex input:

```
Given user hex: #68d391
→ background: rgba(104,211,145,0.12)
→ text: #68d391
→ border: rgba(104,211,145,0.30)
```

This ensures even "loud" user colors are desaturated by opacity, maintaining overall monochrome discipline.

### 2.4 Heatmap Colors

Monthly return heatmap uses a **diverging intensity scale** (not red/green):

| Return | Background | Text |
|---|---|---|
| > +4% | `#38a169` | `#ffffff` |
| > +2% | `#68d391` | `#000000` |
| > 0% | `#9ae6b4` | `#000000` |
| > -2% | `#fc8181` | `#000000` |
| > -4% | `#e53e3e` | `#ffffff` |
| ≤ -4% | `#9b2c2c` | `#ffffff` |

> The heatmap is the one place we use chromatic color — because 12 months × N tickers is too much information to parse without color grouping. Even here, the palette is muted and earthy, not neon.

### 2.5 Body Background Gradient

A nearly-imperceptible radial gradient adds depth without violating the monochrome rule:

```css
background:
  radial-gradient(circle at 80% 0%, rgba(75, 40, 150, 0.18) 0%, transparent 50%),
  radial-gradient(circle at 10% 100%, rgba(15, 110, 140, 0.15) 0%, transparent 50%),
  var(--bg-base);
```

At 0.15–0.18 opacity, this reads as "texture" rather than "purple and teal gradient."

---

## 3. Typography

### 3.1 Font Stack

| Role | Font | Weight | Usage |
|---|---|---|---|
| Display / Headings | Google Sans | 400 | Page titles, card names |
| Body / UI | Google Sans | 400, 500 | Buttons, labels, descriptions |
| Data / Monospace | Google Sans Code | 400 | Prices, returns, ranks, tickers, timestamps |

### 3.2 Type Scale

| Size | Weight | Letter-Spacing | Usage |
|---|---|---|---|
| 32px | 400 | -0.02em | Page title ("MarketDeck") |
| 28px | 400 | -0.01em | List view title |
| 20px | 400 | -0.01em | Watchlist card name |
| 15px | 600 | 0.1em | Modal heading (uppercase) |
| 14px | 400 | 0 | Body text, descriptions |
| 13px | 400 | 0 | Sidebar nav items, button text |
| 12px | 400 | 0 | Ticker badges, input text |
| 11px | 400 | 0.05–0.15em | **Labels** (uppercase, the backbone of the UI) |
| 10px | 400 | 0.08–0.15em | Micro-labels, tag text, footer |

### 3.3 Label Convention

Almost every UI control has an uppercase 11px label above it:

```
LOOKBACK PERIOD          TOP N ASSETS TO HOLD          VIEW
[1M] [3M] [6M] [12M]     [1] [2] [3] [4] [5]          [Rankings] [Monthly Heatmap]
```

This convention:
- Creates vertical rhythm through consistent 10px gap + label height
- Eliminates the need for placeholder text inside inputs
- Makes the UI scannable at a glance

---

## 4. Layout & Spacing

### 4.1 Grid System

| Breakpoint | Layout |
|---|---|
| > 1200px | Sidebar (240px fixed) + Main content (fluid, max 1400px, centered) |
| 832–1200px | Same, but controls reflow to 2×2 grid |
| < 832px | Sidebar becomes slide-out drawer (right side); hamburger menu; single column |

### 4.2 Spacing Scale

Based on an 8px grid:

| Token | Value | Usage |
|---|---|---|
| `space-xs` | 4px | Tight gaps (toggle switches, inline elements) |
| `space-sm` | 8px | Button padding-Y, input internal padding, icon gaps |
| `space-md` | 12px | Card internal padding, table cell padding-Y |
| `space-lg` | 16px | Section gaps, modal internal padding |
| `space-xl` | 24px | Major section separators, sidebar padding |
| `space-2xl` | 32px | Page top padding, card padding, modal padding |
| `space-3xl` | 40px | Main content page padding (desktop) |
| `space-4xl` | 48px | Between major page sections |

### 4.3 Z-Index Hierarchy

| Layer | Z-Index | Elements |
|---|---|---|
| Base | 0–1 | Page content, tables |
| Overlay | 1000 | Editor panel, modals |
| Modal chrome | 1001 | Modal box (above backdrop) |
| Mobile nav | 1050 | Slide-out sidebar |
| Backdrop | 999 | Mobile nav backdrop |
| Hamburger | 1100 | Mobile toggle button |

---

## 5. Component Patterns

### 5.1 Buttons

All buttons share:
- `border-radius: 0` (rectangular)
- `text-transform: uppercase`
- `letter-spacing: 0.1em`
- `font-size: 11px`
- Transparent background + 1px border (default state)
- On hover: invert to solid white background + black text

Variants:

| Variant | Border | Background | Text | Hover |
|---|---|---|---|---|
| Default | `--border-subtle` | transparent | `--text-secondary` | solid white fill, black text |
| Primary | `--text-primary` | transparent | `--text-primary` | solid white fill, black text |
| Destructive | `--accent-negative` | transparent | `--accent-negative` | solid grey fill, black text |
| Muted | `--border-strong` | transparent | `--text-secondary` | elevated surface, white text |
| Active (segmented) | `--text-primary` | `--bg-surface-elevated` | `--text-primary` | — |

### 5.2 Segmented Controls

Used for mutually exclusive choices (lookback period, top N, view tabs):

- Buttons butted against each other with `margin-left: -1px` to collapse borders
- Active state gets `z-index: 2` to render its border above neighbors
- No gap between buttons — reads as a single unified control

### 5.3 Cards

Watchlist cards on the homepage:
- `border-radius: 0`
- `border: 1px solid --border-subtle`
- `background: --bg-surface`
- Hover: `background: --bg-surface-elevated`, `border-color: --border-hover`
- No shadow ever

The "Create New List" card uses a **dashed border** to indicate its different function.

### 5.4 Tables

Two table types:

**Rankings Table:**
- Fixed columns: Rank, Name, Ticker, Type, Return, Price, Signal
- Return column has a mini horizontal bar chart (4px height, no radius)
- Row hover: `rgba(255,255,255,0.02)` background
- Top-N rows get `rgba(255,255,255,0.03)` background (subtle highlight)

**Heatmap Table:**
- Variable columns: Name + 12 months + 12M total
- Each month cell contains a "pill" (actually `border-radius: 6px` — the one exception, to make the color swatch readable)
- Pills use heatmap color scale

### 5.5 Status Bar

A single bar above the data that communicates system state:

| State | Class | Background | Border | Text |
|---|---|---|---|---|
| Loading | `.s-load` | `--bg-surface` | `--border-strong` | `--text-secondary` + spinner |
| Success | `.s-ok` | `--bg-surface-elevated` | `--text-primary` | `--text-primary` |
| Error | `.s-err` | `--bg-surface` | `--accent-negative` | `--accent-negative` |

### 5.6 Modals

- Fixed position, centered with `transform: translate(-50%, -50%)`
- Glass effect: `rgba(255,255,255,0.04)` + `backdrop-filter: blur(16px)`
- `border: 1px solid --border-strong`
- Shadow: `0 30px 80px rgba(0,0,0,0.8)` — the only place shadow is used, and it's deep/black, not colored
- Header has bottom border; actions have top border — frames the content

### 5.7 Editor Panel

A slide-out panel (not a modal) for editing tickers:
- `position: absolute; right: 0; top: 0; bottom: 0`
- `width: 560px` (full width on mobile)
- Same glass treatment as modals
- `border-left` instead of full border

---

## 6. Animation & Motion

### 6.1 Easing

```css
--easing-premium: cubic-bezier(0.16, 1, 0.3, 1);
```

This is an **expo-out** easing — fast start, gentle settle. Feels precise and technical, not bouncy.

### 6.2 Durations

| Token | Duration | Usage |
|---|---|---|
| `--transition-fast` | 0.2s | Button hovers, color changes, border changes |
| `--transition-slow` | 0.4s | Card hovers, sidebar transitions, panel slides |

### 6.3 Specific Animations

| Animation | Implementation | Purpose |
|---|---|---|
| Spinner | CSS `rotate(360deg)` linear infinite, 0.8s | Loading state |
| Mobile sidebar | `transform: translateX(100%) → translateX(0)`, 0.3s ease | Drawer open/close |
| Hamburger → X | CSS transforms on 3 lines (translate + rotate) | Menu toggle feedback |
| Modal backdrop | `opacity` fade | Soft entry, doesn't jar |
| Button hover | `background-color` + `color` swap, 0.2s | Immediate feedback |

### 6.4 What We Don't Animate

- Table row entry/exit (too many rows, would be chaotic)
- Number counting animations (would delay decision-making)
- Page transitions (this is a dashboard, not a slideshow)
- Parallax or scroll-driven effects (no narrative to support)

---

## 7. Responsive Behavior

### 7.1 Desktop (>1200px)

- Full sidebar visible
- Controls in horizontal row
- Watchlist grid: `auto-fill, minmax(320px, 1fr)`
- Tables scroll horizontally if needed

### 7.2 Tablet (832–1200px)

- Sidebar still visible
- Controls reflow to 2×2 grid:
  ```
  [Lookback] [Top N]
  [Filter]   [View]
  ```

### 7.3 Mobile (<832px)

- Sidebar becomes **right-side drawer** (not left — thumb reach on large phones)
- Hamburger button fixed top-right
- Backdrop blur when drawer open
- Single column layout
- Full-width editor panel
- Controls stack vertically
- Table horizontal scroll
- Cards full width

---

## 8. Iconography

We use **zero icon libraries**. All "icons" are:

| Symbol | Usage |
|---|---|
| `+` | Add, create new |
| `✕` | Delete, close, remove |
| `✎` | Edit |
| `←` | Back, breadcrumb |
| `●` / `○` | Buy / Skip signal |
| `↻` | Retry |
| `✓` | Saved confirmation |

These are Unicode characters, not SVG icons. They inherit text color and scale with font-size.

---

## 9. Asset Inventory

### 9.1 Fonts

| Font | Source | Weights Used |
|---|---|---|
| Google Sans | Google Fonts CDN | 400, 500, 600, 700 |
| Google Sans Code | Google Fonts CDN | 400, 700 |

Loaded via:
```html
<link href="https://fonts.googleapis.com/css2?family=Google+Sans:ital,opsz,wght@0,17..18,400..700;1,17..18,400..700&family=Google+Sans+Code:wght@400..700&display=swap" rel="stylesheet">
```

### 9.2 Images

**None.** This application contains no photographs, illustrations, or logos. The "brand" is the data itself.

### 9.3 Dependencies

No frontend framework. No icon library. No charting library (tables are rendered as HTML). The only external dependency is the Google Fonts CDN.

---

## 10. Design Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| Initial | Dark theme | Financial professionals often work at night or in dim offices; dark mode is default in trading terminals |
| Initial | Zero border-radius | Creates a "tool" aesthetic rather than "consumer app"; references Bloomberg, terminal UIs |
| Initial | Monochrome returns | Avoids emotional color triggers; white/grey forces numeric literacy |
| Initial | Uppercase micro-labels | Creates visual hierarchy without size contrast; maximum information density |
| Initial | Glass morphism for modals | Distinguishes overlay from content while maintaining the dark atmosphere |
| Initial | Google Sans | Clean geometric sans with excellent tabular numeral support; "Google Sans Code" gives us a matching monospace |
| Initial | No icons | Every icon would need an SVG; Unicode symbols are sufficient and weightless |
| Initial | Server-side price fetching | Keeps API keys/tokens off the client; enables caching |

---

## 11. Accessibility Notes

- All interactive elements have visible focus states (border color change to white)
- Color is not the sole indicator: positive returns show `+` prefix, buy signals say "BUY" in text
- Tables use proper `<thead>` / `<th>` structure
- Modal traps focus (implemented in JS)
- Mobile hamburger has aria-compatible toggle state
- Scrollbars are custom-styled but maintain sufficient contrast

---

## 12. Future Design Considerations

| Idea | Status | Notes |
|---|---|---|
| Light mode | Considered | Would require inverting the entire palette; not prioritized as target users prefer dark |
| Chart view (line/candlestick) | Considered | Would require a charting library; tables are currently sufficient for the momentum strategy |
| Compact mode | Considered | Could reduce padding by 30% for ultra-dense screens; toggle in settings |
| Custom themes (user-defined) | Considered | Would undermine the monochrome discipline; tag colors are the concession |
| Keyboard shortcuts | Planned | Natural fit for terminal aesthetic; `j/k` navigation, `1-5` for top N, etc. |

---

*Last updated: 2026-05-14*
*Design system version: 1.0*
*Maintainer: Project author*
