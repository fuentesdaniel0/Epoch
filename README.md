# Epoch: Contextual Memory for Claude Code

A session-lifecycle memory protocol for [Claude Code](https://code.claude.com/docs/en/), packaged as a plugin. Project state lives in three version-controlled Markdown files under `.agents/memory/`; four skills read and write them so every session starts with context instead of chat history.

## Problem

AI coding agents lose context between sessions. Dumping raw chat history into the context window causes token bloat, latency, and forgotten architecture.

## Solution

- **Instant Context**: every session starts by reading a concise `context.md`. `/epoch:init` makes that explicit and deterministic.
- **Cheap Milestones**: `/epoch:milestone` appends a dated changelog entry and commits, so progress gets recorded as it happens.
- **Automated Checkpoints**: `/epoch:checkpoint` updates memory, runs the workspace's verification commands, sets the next Session Focus, and commits before you close the session.
- **Self-bootstrapping**: `/epoch:plan` in any directory creates the memory files and interviews you. No copying, no setup script.

## Install (primary path)

Once per machine, inside Claude Code:

```text
/plugin marketplace add fuentesdaniel0/Epoch
/plugin install epoch@epoch
```

Then open any project and run `/epoch:plan`. From a shell the same two steps are `claude plugin marketplace add fuentesdaniel0/Epoch` and `claude plugin install epoch@epoch`.

Updates reach you only when the plugin's manifest `version` is bumped; every Epoch release checkpoint bumps it. Run `/plugin marketplace update` then `/plugin update epoch` to pull a new version.

## Commands

| Command | What it does | Bootstraps blank memory? |
| :--- | :--- | :--- |
| `/epoch:init` | Reads the three memory files and reports architecture, Session Focus, active tasks, last changelog entry. Read-only. | Yes, then reports blank state and hands off to `/epoch:plan`. |
| `/epoch:plan` | Path A interviews you to populate blank memory; Path B grooms the backlog into a sprint. Always stops and waits for your answers. | Yes, then goes straight into the Path A interview. |
| `/epoch:milestone <text>` | Appends a dated entry to `changelog.md`, checks off a matching roadmap item, commits. No verification, no interview. | No. Refuses and points to `/epoch:plan`. |
| `/epoch:checkpoint` | `git status`, memory updates, task migration, changelog rotation, Session Focus interview, verification commands from `context.md`, commit. Never pushes. | No. Refuses and points to `/epoch:plan`. |

Each skill's description is written so Claude also triggers it from natural language ("wrap up the session", "what's the state of the project", "log a milestone"). Per-repo copies of the skills (see fallbacks below) answer to the un-prefixed forms `/init`, `/plan`, `/milestone`, `/checkpoint`.

### How bootstrap works

`init` and `plan` check for `.agents/memory/context.md` in the current directory. When it is missing they write the three blank memory files from templates embedded in the skill itself (a section the sync script generates from `plugin/templates/`, so nothing under the plugin directory has to be readable at runtime), then offer two optional extras: appending a short Epoch block to the project's `CLAUDE.md` (created if absent) and `git init` if the directory is not a repository. Nothing optional is applied without your yes.

### Conditional SessionStart hook

The plugin registers a `SessionStart` hook that checks for `./.agents/memory/context.md`. In an Epoch workspace it injects the Startup SOP reminder (read memory before answering about project state; offer `/epoch:init`). Anywhere else it exits silently, so the plugin costs nothing in projects that do not use it.

## Development loop

1. **Initialize**: `/epoch:init`. First time in a directory it bootstraps and hands off to `/epoch:plan`.
2. **Work**: give Claude tasks. The core directives keep it exploring, verifying, and decomposing.
3. **Milestone**: when something lands, `/epoch:milestone "shipped X"`. Cheap enough to run often.
4. **Checkpoint**: `/epoch:checkpoint` at the end of the session. Verification comes from `## Verification Commands` in `context.md`.
5. **Fresh session**: `/clear` or a new `claude` process. The hook reminds Claude to read memory; `/epoch:init` restores state.

## Fallbacks without the plugin

**Bootstrap a workspace from this repo:**

```bash
python3 scripts/create-workspace.py /path/to/new-project
```

Copies `template/` into the target, asks for a project name, domain, and verification commands, writes them into `context.md`, then `git init` and first commit. Flags `--name`, `--domain`, `--verify CMD`, `--no-git` make it non-interactive.

**Copy the folder into an existing project:**

```bash
cp -a template/CLAUDE.md template/.claude template/.agents /path/to/existing-project/
```

Both fallbacks give you un-prefixed `/init`, `/plan`, `/milestone`, `/checkpoint` plus a `SessionStart` hook in `.claude/settings.json`.

## Repository layout

```text
plugin/                        # THE engine. Single source of truth.
  .claude-plugin/plugin.json   # manifest (version 2.1.0)
  skills/<name>/SKILL.md       # init, plan, checkpoint, milestone, scaffold-module
  hooks/hooks.json             # conditional SessionStart hook
  templates/memory/            # blank context.md, backlog.md, changelog.md
  templates/CLAUDE.snippet.md  # block offered for a project's CLAUDE.md
  evals/                       # claude plugin eval suite (four cases)
.claude-plugin/marketplace.json  # self-hosted marketplace: plugin "epoch" -> ./plugin
template/                      # GENERATED copy-a-folder distribution (CLAUDE.md, .claude/, .agents/memory/)
CLAUDE.md, .claude/, .agents/  # GENERATED dogfood instance tracking Epoch's own development
scripts/sync-templates.py      # plugin/ -> template/ -> root. Idempotent. The only propagation path.
scripts/create-workspace.py    # template/ -> new project
EVALUATION.md                  # manual behavioral test script
```

Edit skills only under `plugin/skills/`, then run `python3 scripts/sync-templates.py`. Root memory files are never overwritten by sync.

## Contributing and releasing

1. Change files under `plugin/`, run `python3 scripts/sync-templates.py`, commit.
2. `claude plugin validate --strict ./plugin` and `claude plugin validate --strict .` must pass.
3. Pre-release gate: `claude plugin eval ./plugin --scaffold --allow-tools Bash Write Edit --trust-plugin --no-publish` (see `plugin/evals/README.md`).
4. Bump `version` in `plugin/.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, then `/epoch:checkpoint`.

Community marketplace submission (owner action): individual authors use the Console form at platform.claude.com/plugins/submit after `claude plugin validate ./plugin` passes.

## Roadmap

Claude Code is the only supported harness. The state files in `.agents/memory/` are deliberately harness-neutral, so adapters for other assistants are planned as thin engine ports over the same memory.
