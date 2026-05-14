# Git Wrangler Design System

> A design document for the CLI orchestrator and its documentation hub.
> Last updated: 2026-05-14

---

## 1. Design Philosophy

### 1.1 Core Tenet: Invisible Infrastructure

Git Wrangler is built on the principle that **the best tooling disappears**. Like a skilled stagehand, it operates behind the scenes—broadcasting Git operations across repositories so developers can focus on writing code, not managing repositories.

This philosophy manifests in three ways:

1. **Zero Configuration by Default**: Install, run, succeed. No config files, no setup ceremonies, no state management beyond Git itself.
2. **Familiar Grammar**: Commands mirror Git's own vocabulary (`pull`, `push`, `commit`, `status`). The learning curve is flattened because the mental model already exists.
3. **Clear, Scannable Output**: Operations across N repositories produce output that is immediately scannable. Colors carry semantic meaning; structure carries categorical meaning.

### 1.2 The Wrangler Metaphor

The name "Wrangler" evokes herding—corraling scattered repositories into orderly formation. This metaphor informs:

- **Collective action**: Operations apply to groups, not individuals
- **Gentle force**: History rewriting is powerful but guarded behind explicit flags and confirmations
- **Range work**: The tool covers a wide territory (local ops, remote ops, history rewriting, utilities)

### 1.3 Safety Through Isolation

Every repository operation runs in a subshell. This is not merely an implementation detail—it is a **design guarantee**:

- Directory changes never leak
- Variable mutations never leak
- Failure in one repository never aborts the entire run (unless explicitly requested)

This design choice makes parallel-like execution mentally modelable: each repository is its own universe.

---

## 2. CLI Design System

### 2.1 Command Taxonomy

Commands are organized into four categories that reflect the developer workflow lifecycle:

| Category | Purpose | Mental Model |
|---|---|---|
| **Remote Operations** | Sync with GitHub | "Talk to the server" |
| **Local Operations** | Modify working state | "Work on my machine" |
| **History Rewriting** | Alter commit history | "Time travel (dangerous)" |
| **Utility** | Introspection and maintenance | "Tool administration" |

This taxonomy is enforced by the `Category:` metadata field in each script's header block. The help system uses it to group commands dynamically.

### 2.2 Naming Conventions

- **Commands use kebab-case**: `rewrite-authors`, `fix-gitignore`, `rename-repo`
- **Flags use double-dash long-form**: `--message`, `--rebase`, `--into`
- **No short flags**: This is intentional. Short flags save keystrokes at the cost of memorization. Git Wrangler favors explicitness over brevity because the target user is often running a command once across many repos, not repeatedly in a tight loop.

### 2.3 Output Formatting

#### Color Semantics

Color is not decorative—it carries semantic weight:

| Color | ANSI Code | Meaning |
|---|---|---|
| **Red** | `\\e[31m` | Errors, failures, fatal conditions |
| **Green** | `\\e[32m` | Success, completion, affirmative states |
| **Yellow** | `\\e[33m` | Warnings, skipped operations, "no changes needed" |
| **Blue** | `\\e[34m` | Category headers, structural information |
| **Bold** | `\\e[1m` | Labels, emphasis, section headers |
| **Reset** | `\\e[0m` | Always terminate colored strings |

**Rule**: Every `printf` with color MUST end with `\\e[0m`. Every error message MUST be redirected to stderr (`>&2`).

#### Output Structure

For operations across multiple repositories, output follows a consistent pattern:

```
[repo-name]    Status message
[repo-name]    Success message
[repo-name]    Warning: explanation
```

The repository name is left-aligned and acts as a prefix, creating an implicit column that makes scanning easy.

### 2.4 Error Handling Philosophy

1. **Capture before display**: Command output (stdout and stderr) is captured into a variable first. It is only displayed if the command fails.
2. **Never let output bleed**: Unexpected command output never pollutes the terminal. This preserves the scannable columnar format.
3. **Fail explicit, fail helpful**: Error messages include the repository name, the operation that failed, and the raw error output.

Example:
```bash
if command_output=$(git commit -m "Message" 2>&1); then
    printf "Commit successful for %s\n" "$repo_name_display"
else
    printf "Error: Commit failed for %s:\n%s\n\n" "$repo_name_display" "$command_output" >&2
fi
```

### 2.5 The Header Block Convention

Every subcommand script begins with a structured comment block:

```bash
# ====
# Usage: git-wrangler <subcommand> [--arg1 <value>] [--flag]
# Description: Brief one-line explanation of the subcommand's purpose.
# Category: Remote Operations | Local Operations | History Rewriting | Utility
#
# One or more sentences explaining what the subcommand does, any important
# prerequisites, and its default behaviour.
#
# Options:
#   --flag1 <value>  (required) What this flag does.
#   --flag2          (optional) What this flag does.
#
# Example:
#     git-wrangler <subcommand> --flag1 value
# ====
```

This block serves as both **documentation** (rendered by `git-wrangler help`) and **metadata** (used for dynamic discovery). No central registry exists—this is decentralized documentation.

---

## 3. Architecture Design

### 3.1 The Dispatcher Pattern

The root `git-wrangler` script is a **thin router**. It does nothing except validate the subcommand name and `exec` the corresponding script in `libexec/`.

```
git-wrangler <subcommand> [args...]
         |
         v
   libexec/git-wrangler-<subcommand>
```

**Design rationale**:
- **Extensibility**: Adding a command means adding a file. No registry edits.
- **Isolation**: Each command is a standalone executable. Bugs in one command cannot corrupt another.
- **Transparency**: Users can read any command's source directly.

### 3.2 Dynamic Discovery

The help system discovers commands by listing files in `libexec/` matching the pattern `git-wrangler-*`. This means:

- New commands appear in help automatically
- Deleted commands disappear automatically
- No orphaned registry entries

### 3.3 Subshell Isolation

When iterating over repositories, the loop body is wrapped in a subshell:

```bash
while IFS= read -r git_dir; do
    (
        repo_dir=$(dirname "$git_dir")
        cd "$repo_dir" || exit
        # ... logic ...
    )
done <<< "$git_repositories"
```

**Why a here-string instead of a pipe?**
Pipes create subshells that destroy variable mutations. Here-strings (`<<<`) keep the loop in the parent shell while the explicit subshell `( ... )` provides controlled isolation for `cd` operations.

### 3.4 Target Discovery

Repository discovery uses `find` with **no artificial depth limits** (unless strictly looking for top-level `.git/` roots). This ensures nested repositories are never silently missed.

```bash
git_repositories=$(find . -type d -name ".git" 2>/dev/null)
```

If no repositories are found, the script exits gracefully with a yellow informational message—not an error.

---

## 4. Visual Identity

### 4.1 Connection to the Website

The CLI's visual identity is intentionally **terminal-native**: it uses standard ANSI colors that work in any terminal emulator. The website (`website/`) translates this terminal aesthetic into a premium web experience using the Vercel/Geist design system.

The bridge between CLI and web:

| CLI Element | Web Equivalent |
|---|---|
| Red error output | `--color-ship` (`#ff5b4f`) for urgent states |
| Green success output | `--color-develop` (`#0a72ef`) mutated to success green in terminal context |
| Blue category headers | Geist Mono uppercase labels |
| Bold labels | Weight 600 typography |
| Columnar output | Grid layouts with consistent alignment |

### 4.2 Logo and Brand Assets

- **Logo**: `website/public/git-wrangler.svg` and `git-wrangler.png`
- **Favicon**: `website/public/favicon.svg`
- **Brand color**: The CLI has no single brand color—it uses semantic colors. The website anchors on Vercel Black (`#171717`) as the primary identity color.

### 4.3 Terminal Aesthetic on the Web

The website features a **terminal component** (`.terminal` in `global.css`) that renders fake terminal output with macOS window chrome (red/yellow/green dots). This creates continuity between the CLI product and its marketing surface.

---

## 5. Design Principles and Constraints

### 5.1 Principles

1. **Explicit over implicit**: Long flags, clear error messages, no magic behavior
2. **Safe over convenient**: Subshell isolation, captured output, dry-run modes where applicable
3. **Scannable over beautiful**: Output is optimized for reading at a glance across many repositories
4. **Flat over nested**: No sub-subcommands. The command namespace is flat and discoverable.
5. **Filesystem over database**: State lives in Git, not in a proprietary database or config file

### 5.2 Constraints

1. **Bash 4+ only**: No POSIX sh compatibility. Bash arrays, `[[` tests, and `printf -v` are all fair game.
2. **No external dependencies for core**: Only `git` is required for basic operations. `gh` and `git-filter-repo` are required only for specific commands.
3. **No background processes**: Commands run sequentially within each repository. Parallelism is left to the user's shell if desired.
4. **No state files**: Git Wrangler does not maintain a database, config file, or lockfile. All state is derived from the filesystem at runtime.

### 5.3 Adding a New Command

To add a new subcommand:

1. Create `libexec/git-wrangler-<name>` (no `.sh` extension)
2. Include the standard header block (see §2.5)
3. Follow the standard script structure:
   - Shebang (`#!/bin/bash`)
   - Header block with Usage/Description/Category
   - Variable defaults and argument parsing (`while [[ $# -gt 0 ]]`)
   - Prerequisite checks (`command -v`)
   - Target discovery (`find`)
   - Execution loop (`while IFS= read -r` with `<<<`)
   - Colored output using the semantic color system
4. No registration step is needed—the help system discovers it automatically

---

## 6. Documentation Design

### 6.1 Dual Documentation

Git Wrangler has two documentation surfaces:

1. **In-CLI help**: Embedded in script headers, rendered by `git-wrangler help`
2. **Website docs**: Astro Content Collections in `website/src/content/docs/`

These should stay synchronized. The website docs provide long-form explanations; the CLI help provides quick reference.

### 6.2 Documentation Categories

Website docs mirror the CLI command categories:

| CLI Category | Docs Section |
|---|---|
| Remote Operations | `clone.md`, `pull.md`, `push.md`, `rename-repo.md` |
| Local Operations | `commit.md`, `review.md`, `license.md`, `untrack.md`, `fix-gitignore.md`, `rename-branch.md`, `reset.md` |
| History Rewriting | `rewrite-authors.md`, `rewrite-commits.md`, `rewrite-dates.md`, `remove-secrets.md` |
| Utility | `status.md`, `info.md`, `update.md`, `uninstall.md`, `help.md` |

Cross-cutting topics (`installation.md`, `architecture.md`, `introduction.md`) live outside the category structure.

---

## 7. Anti-Patterns

The following are explicitly **not** how Git Wrangler works. These constraints are documented to prevent well-intentioned contributions from drifting away from the design philosophy.

| Anti-Pattern | Why We Avoid It |
|---|---|
| Central command registry | Violates dynamic discovery; creates maintenance burden |
| Short flags (`-m` instead of `--message`) | Saves 4 keystrokes, costs memorization. Explicitness > brevity. |
| Piping into `while read` | Creates subshells that destroy variable state |
| Bare `read` without `-r` | Mangles Windows paths with backslashes |
| `echo "$var"` | Triggers `echo` flags if variable starts with `-` |
| `git ls-files` for existence checks | Only checks the index; misses untracked files |
| Hardcoded `find -maxdepth` | Silently misses nested matches unless strictly intended |
| Decorative colors | Every color must carry semantic meaning |
| Background/daemon processes | Adds complexity; sequential execution is predictable |
| Config files or state databases | Violates "filesystem over database" principle |

---

## 8. Evolution Guidelines

When extending Git Wrangler:

1. **Preserve the flat namespace**: If a command feels like it needs subcommands, it should probably be multiple top-level commands or the scope is too broad.
2. **Preserve semantic color**: New output must follow the red/green/yellow/blue convention.
3. **Preserve subshell isolation**: Any loop over repositories must wrap the body in `( ... )`.
4. **Preserve dynamic discovery**: New commands need no registration, but they MUST have a valid `Category:` in their header.
5. **Preserve zero-config defaults**: A user should be able to run a new command immediately after installation with no setup.

---

*This document is a living specification. When the project's behavior changes, this document should be updated to reflect the new design truth.*
