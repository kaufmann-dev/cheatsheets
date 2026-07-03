# AGENTS.md

## Repo type

Static personal knowledge base. No build system, no package manager, no tests, no CI.

## Structure

- `commands/` — CLI tool reference sheets (ffmpeg, linux, imagemagick, etc.)
- `designs/` — design system specs with YAML frontmatter token definitions
- `guides/` — step-by-step guides
- `utilities/` — standalone helper scripts and browser utilities (Python, Bash, JS)

## What to know

- There is no `package.json`, `Makefile`, or any build toolchain. Don't look for one.
- There is no test runner, linter, or formatter. No verification commands to run.
- No CI/CD. No git hooks (only `.sample` hooks present).
- The standalone scripts in `utilities/` have no dependency management — each documents its own external requirements (e.g., `ffmpeg`).