---
name: init
description: Read the Epoch memory files and report the current project state (bootstraps blank memory in a new directory). Use when the user asks "what's the state of the project", "where were we", "what's next", "catch me up", "sync state", "what am I working on", or wants orientation at the start of a session. Read-only; never modifies files.
disable-model-invocation: false
---

# Initialize: Deterministic Startup SOP

> Invoked as `/epoch:init` from the Epoch plugin, or `/init` from a per-repo copy of this skill. The steps are identical.

Workspace memory: !`[ -f .agents/memory/context.md ] && echo present || echo ABSENT`

This is the explicit form of the Startup SOP in `CLAUDE.md`. Execute it in exactly this order and **never modify an existing file**. The only writes this skill may make are the bootstrap copies in step 0, and only when memory is absent.

## 0. Bootstrap check

- If the line above says `present`, skip to step 1. (Per-repo copies of this skill always take this branch.)
- If it says `ABSENT`, this directory is not yet an Epoch workspace. Say so in one sentence, then create the memory from the plugin's bundled templates with `Bash`:

```bash
mkdir -p .agents/memory && cp "${CLAUDE_PLUGIN_ROOT}/templates/memory/"*.md .agents/memory/
```

  If `${CLAUDE_PLUGIN_ROOT}` is not set or the copy fails (this skill is running outside the plugin), stop and tell the user to copy Epoch's `template/.agents/memory/` into `.agents/memory/` instead; do not hand-write memory files.
- Offer, but do not apply unasked, two one-line extras in your next message: (a) append `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.snippet.md` to the project's `CLAUDE.md` (create it if absent); (b) `git init` if `git rev-parse --is-inside-work-tree` fails. Apply whichever the user accepts.
- After a bootstrap, the memory is blank by definition: read the files (step 1), then take the uninitialized branch of step 2, and include the two extras above in the same handoff message.

## 1. Read all three memory files

- `Read` `.agents/memory/context.md`
- `Read` `.agents/memory/backlog.md`
- `Read` `.agents/memory/changelog.md`

If any file is missing, stop and report which one, then run the bootstrap in step 0 for the missing file.

## 2. Detect blank templates

The memory is **uninitialized** if `context.md` still has an empty "Active Stack Details" table, the `project` frontmatter key is empty, or `backlog.md` still contains bracketed placeholders such as `[Name of Next Major Objective]` or the line "Unassigned - Run `/epoch:plan`".

If uninitialized: say plainly that the memory files are blank templates, and hand off to `/epoch:plan` (Path A: New Project Intake). Do not invent a project state.

## 3. Report (if initialized)

Present a concise state report with these four sections, quoting the files rather than paraphrasing loosely:

1. **Architecture snapshot**: the project name and domain from `context.md` frontmatter, the stack table, and the module descriptions in one or two lines each.
2. **Session Focus**: the checklist under "Session Focus" in `backlog.md`, verbatim.
3. **Active backlog tasks**: the "Active Backlog Tasks" list, verbatim.
4. **Last changelog entry**: the heading and the Accomplishment/Decisions bullets of the most recent entry in `changelog.md`.

Also note whether `## Verification Commands` in `context.md` is populated, so the user knows what `/epoch:checkpoint` will run.

## 4. Handoff

End by asking whether to start on the Session Focus, or to run `/epoch:plan` to groom the backlog first. Then stop and wait for the user.
