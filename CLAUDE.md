# Epoch Memory Protocol

This repository runs **Epoch**: a Markdown protocol that gives Claude Code persistent, stateful memory across sessions through version-controlled files. All project state lives in `.agents/memory/`. This file and `.claude/` are only the engine that reads and writes that state; never keep state anywhere else.

## Startup SOP (every new session)

1. Silently read `.agents/memory/context.md` to align with the active stack, architecture, and rules.
2. Silently read the **Session Focus** section at the top of `.agents/memory/backlog.md`.
3. If the backlog has a focus or active tasks, summarize the Session Focus in one or two lines and ask whether to begin, or to run `/plan` to groom the backlog. If the memory files are still blank templates, say so and propose `/plan`.
4. Never answer questions about project state from guesswork. If you have not read the memory files this session, read them first.

## Memory map

- `.agents/memory/context.md`: active state, stack, architecture / code graph, environment notes, verification commands.
- `.agents/memory/backlog.md`: Session Focus (top), high-level roadmap, active backlog tasks.
- `.agents/memory/changelog.md`: chronological history of sprints, milestones, and decisions. Old entries rotate to `.agents/memory/archive/`.

## Commands

- `/init`: read all three memory files and report the current state. Read-only.
- `/plan`: interactive. Path A initializes a new project by interview; Path B grooms the backlog into a sprint.
- `/milestone <description>`: append a dated changelog entry and commit. Cheap: no verification, no interview.
- `/checkpoint`: full session wrap-up. Memory updates, verification, Session Focus interview, commit (never push).

## Operating discipline

Follow `.claude/rules/core-directives.md` (loaded automatically): explore before editing, verify continuously, work in atomic steps. Commit only when a skill says to. Never push unless the user explicitly asks.
