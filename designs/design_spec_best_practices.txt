# DESIGN.md Specifications and Best Practices

This document outlines the general rules, specifications, and best practices for creating a compliant `DESIGN.md` file based on the official design specification standard.

## 1. YAML Front Matter Integration
- **Mandatory YAML Header:** Every `DESIGN.md` must begin with a YAML front matter block delimited by `---` fences. This separates machine-readable design tokens from the contextual, human-readable prose.
- **Top-level Fields:** Include a `version` field (e.g., `version: alpha`) and a `description` field providing a high-level system overview.
- **Token Schemas:** The YAML block must contain structured schemas for `colors`, `typography`, `spacing`, `rounded`, and `components`.

## 2. Design Tokens Syntax & Schema
- **Colors:**
  - Define all color tokens as hex strings. Do not use `rgba()` or other formats as they are not valid token types. Opacity-based logic should be explained in the prose sections.
  - Use role-based naming (e.g., `primary`, `secondary`, `on-surface`, `surface-container`) rather than arbitrary CSS-style names (e.g., `--text-secondary`).
- **Typography:**
  - Rename tokens to semantic scale names (e.g., `headline-xl`, `body-md`, `label-md`) instead of generic HTML elements (e.g., `h1`, `body`).
  - Use specific, machine-parseable properties: `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, and `letterSpacing`.
  - Avoid dual-notation sizes (e.g., "2.5rem (40px)"); use single Dimension values instead.
  - Do not include `color` as a property under typography tokens.
- **Dimensions & Spacing:** All dimension values (for `fontSize`, `spacing`, `rounded`) must include exact units (e.g., `px`, `rem`, `ch`) to allow for linter validation. Avoid relative or descriptive text for dimensions.
- **Shapes & Rounded:** Standardize rounded tokens to scale levels (`sm`, `md`, `lg`, `full`) instead of element-specific names (e.g., `buttons`, `tags`).
- **Components:**
  - Define UI primitives (`button-primary`, `tag`, `navbar`, `card`) in the `components:` block.
  - Define specific component design values (padding, height, roundedness) within the YAML to ensure interoperability with CLI tools and code generation.

## 3. Section Standardization and Ordering
- **Canonical Section Order:** The document must strictly adhere to the following sequence of headers (without numbering):
  1. `## Brand & Style` (or `## Overview`)
  2. `## Colors`
  3. `## Typography`
  4. `## Layout & Spacing`
  5. `## Elevation & Depth`
  6. `## Shapes`
  7. `## Components`
  8. `## Do's and Don'ts`
- **Consolidation of Content:**
  - Remove non-standard top-level headers (e.g., "Design Philosophy", "Component Patterns").
  - Migrate "Core Assets" into the "Overview" and "Colors" sections.
  - Place "Animation & Motion", "Accessibility", and "Asset Guidelines" as subsections under "Components".
  - Merge "Responsive Breakpoints" into the "Layout & Spacing" section.
  - Consolidate "Design Decisions", "Iconography & Graphics" rules, and "Anti-Patterns" into the final "Do's and Don'ts" section.

## 4. Markdown Formatting & Token Referencing
- **Token Binding:** Replace hardcoded design values in the Markdown prose with dynamic token references using the `{path.to.token}` syntax (e.g., `{rounded.sm}` instead of `4px`, or `backgroundColor: "{colors.primary}"`).
- **Consistency:** Ensure linter validation can tie component styles to the base palette.
- **Agent Optimization:** The document should be explicitly optimized for reading by coding agents by cleanly separating normative, machine-readable values (YAML) from their contextual rationale (Prose).
