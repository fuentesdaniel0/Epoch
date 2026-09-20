---
name: init
description: Read the Epoch memory files and report the current project state. Use when the user asks "what's the state of the project", "where were we", "what's next", "catch me up", "sync state", "what am I working on", or wants orientation at the start of a session. Read-only; never modifies files.
disable-model-invocation: false
---

# Initialize: Deterministic Startup SOP

This is the explicit form of the Startup SOP in `CLAUDE.md`. Execute it in exactly this order and **never modify any file**.

## 1. Read all three memory files
- `Read` `.agents/memory/context.md`
- `Read` `.agents/memory/backlog.md`
- `Read` `.agents/memory/changelog.md`

If any file is missing, stop and report which one, then suggest copying it from Epoch's `template/.agents/memory/`.

## 2. Detect blank templates
The memory is **uninitialized** if `context.md` still has an empty "Active Stack Details" table, the `project` frontmatter key is empty, or `backlog.md` still contains bracketed placeholders such as `[Name of Next Major Objective]` or the line "Unassigned - Run `/plan`".

If uninitialized: say plainly that the memory files are blank templates, and hand off to `/plan` (Path A: New Project Intake). Do not invent a project state.

## 3. Report (if initialized)
Present a concise state report with these four sections, quoting the files rather than paraphrasing loosely:

1. **Architecture snapshot**: the project name and domain from `context.md` frontmatter, the stack table, and the module descriptions in one or two lines each.
2. **Session Focus**: the checklist under "Session Focus" in `backlog.md`, verbatim.
3. **Active backlog tasks**: the "Active Backlog Tasks" list, verbatim.
4. **Last changelog entry**: the heading and the Accomplishment/Decisions bullets of the most recent entry in `changelog.md`.

Also note whether `## Verification Commands` in `context.md` is populated, so the user knows what `/checkpoint` will run.

## 4. Handoff
End by asking whether to start on the Session Focus, or to run `/plan` to groom the backlog first. Then stop and wait for the user.
