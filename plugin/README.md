# Epoch plugin for Claude Code

Session-lifecycle memory protocol: `init`, `plan`, `checkpoint`, `milestone`. Persistent project state in versioned Markdown under `.agents/memory/`, bootstrapped on demand in any directory.

## Install

Once per machine, inside Claude Code:

```text
/plugin marketplace add fuentesdaniel0/Epoch
/plugin install epoch@epoch
```

Then, in any project directory, run `/epoch:plan`. For local development of the plugin itself:

```bash
claude --plugin-dir ./plugin
```

## Commands

| Command | Behavior | Bootstraps? |
| :--- | :--- | :--- |
| `/epoch:init` | Reads the three memory files and reports architecture, Session Focus, active tasks, last changelog entry. Read-only. | Yes: creates blank memory, then reports it as blank and hands off to `/epoch:plan`. |
| `/epoch:plan` | Path A interviews you to populate blank memory; Path B grooms the backlog into a sprint. Always stops and waits for answers. | Yes: creates blank memory, then goes straight into the Path A interview. |
| `/epoch:milestone <text>` | Appends a dated changelog entry, checks off a matching roadmap item, commits. No verification, no interview. | No: refuses and points to `/epoch:plan`. |
| `/epoch:checkpoint` | Memory updates, task migration, changelog rotation, Session Focus interview, verification commands from `context.md`, commit. Never pushes. | No: refuses and points to `/epoch:plan`. |

`scaffold-module` is also included as a model-invoked skill for creating new modules.

## How bootstrap works

`init` and `plan` check for `.agents/memory/context.md` in the current directory. When it is missing they copy the three blank memory files from this plugin's `templates/memory/` (resolved through `${CLAUDE_PLUGIN_ROOT}`), then offer two optional extras: appending a short Epoch block to the project's `CLAUDE.md`, and `git init` if the directory is not a repository. Neither extra is applied without your yes.

`checkpoint` and `milestone` never bootstrap. Checkpointing a workspace that has no memory is refused rather than invented.

## SessionStart hook

`hooks/hooks.json` registers a `SessionStart` hook that checks for `./.agents/memory/context.md`. In an Epoch workspace it injects the Startup SOP reminder. Anywhere else it exits 0 with no output, so the plugin is silent in projects that do not use it.

## Updates

Users receive plugin updates only when `version` in `.claude-plugin/plugin.json` is bumped. Every release checkpoint of the Epoch repo bumps it.

## Layout

```text
plugin/
├── .claude-plugin/plugin.json   # manifest (the only file that belongs in .claude-plugin/)
├── skills/<name>/SKILL.md       # init, plan, checkpoint, milestone, scaffold-module
├── hooks/hooks.json             # conditional SessionStart hook
├── templates/memory/            # blank context.md, backlog.md, changelog.md
├── templates/CLAUDE.snippet.md  # block offered for the project's CLAUDE.md
└── evals/                       # claude plugin eval suite
```

This directory is the single source of truth for the Epoch engine. The repo's `scripts/sync-templates.py` generates the copy-a-folder `template/` and the repo's own dogfood instance from it.
