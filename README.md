# Epoch: Contextual Memory for Claude Code

A drop-in Markdown protocol that gives [Claude Code](https://code.claude.com/docs/en/) persistent, stateful memory across sessions. Zero databases: state is three version-controlled Markdown files, and the engine is a `CLAUDE.md` plus a handful of native Claude Code skills.

## Problem

AI coding agents lose context between sessions. Dumping raw chat history into the context window causes token bloat, latency, and forgotten architecture.

## Solution

A version-controlled file structure that synchronizes the agent's state:

- **Instant Context**: every session starts by reading a concise `context.md` instead of parsing chat history. `/init` makes that explicit and deterministic.
- **Cheap Milestones**: `/milestone` appends a dated changelog entry and commits, so progress gets recorded as it happens.
- **Automated Checkpoints**: `/checkpoint` updates memory, runs the workspace's verification commands, sets the next Session Focus, and commits before you close the session.
- **Ambient Discipline**: `.claude/rules/core-directives.md` enforces explore-before-edit, verify-continuously, atomic-steps behavior every session.

## Repository Layout

```
CLAUDE.md                    # protocol entry point: Startup SOP, memory map, command index
.claude/
  rules/core-directives.md   # operating discipline, loaded every session
  skills/
    init/SKILL.md            # /init       read-only state report
    plan/SKILL.md            # /plan       interview-driven project intake or sprint planning
    milestone/SKILL.md       # /milestone  append + commit a milestone
    checkpoint/SKILL.md      # /checkpoint full session wrap-up
    scaffold-module/SKILL.md # boilerplate for a new module
  settings.json              # SessionStart hook reinforcing the Startup SOP
.agents/
  memory/                    # STATE (harness-neutral)
    context.md               # active stack, architecture, environment, verification commands
    backlog.md               # Session Focus, roadmap, active tasks
    changelog.md             # chronological history; rotated into memory/archive/
```

Two more directories exist only in this repository: `template/` is the pristine source of truth for the engine and blank memory files, and `scripts/` holds the tooling below. The root `CLAUDE.md`, `.claude/`, and `.agents/memory/` are the live, dogfooded instance that tracks Epoch's own development.

## Quick Start

### Path A: Bootstrap a new workspace

```bash
python3 scripts/create-workspace.py /path/to/new-project
```

The script copies `template/` into the target, asks for a project name, a one-line domain, and the verification commands `/checkpoint` should run, writes those into `context.md`, then runs `git init` and makes the first commit. Flags (`--name`, `--domain`, `--verify CMD`, `--no-git`) make it non-interactive.

### Path B: Drop into an existing project

```bash
cp -a template/CLAUDE.md template/.claude template/.agents /path/to/existing-project/
```

Then open Claude Code in that directory and run `/init`. It will tell you the memory is blank and hand off to `/plan`.

## Commands

| Command | What it does | Modifies files? |
| :--- | :--- | :--- |
| `/init` | Reads all three memory files and reports architecture, Session Focus, active tasks, last changelog entry. Hands off to `/plan` if memory is blank. | No |
| `/plan` | Path A interviews you to populate blank memory. Path B reviews the backlog and grooms a sprint. Always stops and waits for your answers. | Yes |
| `/milestone <text>` | Appends a dated entry to `changelog.md`, checks off a matching roadmap item, commits. No verification, no interview. | Yes |
| `/checkpoint` | `git status`, memory updates, task migration, changelog rotation, Session Focus interview, verification commands from `context.md`, commit. Never pushes. | Yes |

Each skill's description is written so Claude also triggers it from natural language ("wrap up the session", "what's the state of the project", "log a milestone").

## Development Loop

1. **Initialize**: start `claude`, run `/init`. First time, it hands off to `/plan` to fill the memory.
2. **Work**: give Claude tasks. The core directives keep it exploring, verifying, and decomposing.
3. **Milestone**: when something lands, `/milestone "shipped X"`. Cheap enough to run often.
4. **Checkpoint**: `/checkpoint` at the end of the session. Verification comes from `## Verification Commands` in `context.md`.
5. **Fresh session**: `/clear` or a new `claude` process. Run `/init` and continue with zero token bloat.

## Keeping the template in sync

`template/` is the source of truth. After editing it, run:

```bash
python3 scripts/sync-templates.py
```

It overwrites the root `CLAUDE.md` and `.claude/**`, never overwrites `.agents/memory/**`, and is idempotent.

## Customization

- Put the project's build, lint, and test commands under `## Verification Commands` in `.agents/memory/context.md`.
- Add project-specific rules as extra files in `.claude/rules/`.
- Adjust or add skills under `.claude/skills/`; each `SKILL.md` needs only `name` and `description` frontmatter.

## Roadmap

Claude Code is the only supported harness today. The state files in `.agents/memory/` are deliberately harness-neutral, so adapters for other assistants are planned as thin engine ports over the same memory.
