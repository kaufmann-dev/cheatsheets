# AGENTS.md

## Repo type

Static personal knowledge base. No build system, no package manager, no tests, no CI.

## Structure

- `commands/` — CLI tool reference sheets (ffmpeg, linux, imagemagick, etc.)
- `designs/` — design system specs with YAML frontmatter token definitions
- `guides/` — step-by-step guides
- `prompts/` — copy-paste AI prompt templates
- `snippets/` — standalone scripts (Python, Bash, JS)

## What to know

- There is no `package.json`, `Makefile`, or any build toolchain. Don't look for one.
- There is no test runner, linter, or formatter. No verification commands to run.
- No CI/CD. No git hooks (only `.sample` hooks present).
- The standalone scripts in `snippets/` have no dependency management — each documents its own external requirements (e.g., `ffmpeg`, `jQuery`).

## Prompt Structure

When creating or modifying prompts in the `prompts/` directory, you MUST strictly adhere to the following standardized format. Do not use Markdown headings inside the prompt itself; use the plain text labels as shown below.

```text
You are a [Role].

[Task Statement - One sentence primary action]

Goal:
[One sentence clear objective summary]

Rules:
- [Rule 1: Hard constraint or preference]
- [Rule 2: Lowercase, dash-bulleted list]
- [Rule 3: Keep rules concise and actionable]

Process:
1. [Step 1: First action to take]
2. [Step 2: Numbered, step-by-step logic map]
3. [Step 3: Sequential instructions for the AI]

Output:
[Format instructions]

[Negative constraints/Final tips]
```
