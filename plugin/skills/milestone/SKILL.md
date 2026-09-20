---
name: milestone
description: Record a completed milestone with a dated changelog entry and a commit, without the full checkpoint ceremony. Use when the user says "log a milestone", "record that we finished X", "note this in the changelog", "mark X done", or invokes /epoch:milestone <description>. Cheap and fast; no verification, no interview.
argument-hint: [description of the milestone]
---

# Milestone Capture

> Invoked as `/epoch:milestone` from the Epoch plugin, or `/milestone` from a per-repo copy of this skill. The steps are identical.

Workspace memory: !`[ -f .agents/memory/context.md ] && echo present || echo ABSENT`

## 0. Precondition: Epoch workspace required

- If the line above says `ABSENT`, stop immediately. Reply: *"This directory is not an Epoch workspace (no `.agents/memory/context.md`). Run `/epoch:plan` to bootstrap it first."* Do **not** create memory files, do **not** guess state, and do **not** commit anything.
- If it says `present`, continue.

Today's date: !`date +%Y-%m-%d`

Milestone to record: **$ARGUMENTS**

If no description was given, ask the user for a one-line description, then stop and wait. Otherwise proceed without further questions.

## 1. Append to the changelog

- `Read` `.agents/memory/changelog.md`.
- Append a new entry at the end of the timeline (below the last entry, above nothing else) in this exact shape:

```markdown
### Milestone (YYYY-MM-DD): <description>
* **Accomplishment**: <one or two sentences, expanded from the description and your knowledge of this session's work>
```

Use today's date shown above. Keep the entry short; this is a marker, not a sprint narrative.

## 2. Optionally check off the roadmap item

- `Grep` `.agents/memory/backlog.md` for a "High-Level Roadmap" feature whose text clearly matches the milestone description.
- If exactly one unambiguous match exists, mark it `[x]`. If none or several match, leave the backlog untouched and mention that in your reply.

## 3. Commit (never push)

- If the workspace is a git repository (`git rev-parse --is-inside-work-tree`):
  - `git add .agents/memory/changelog.md .agents/memory/backlog.md`
  - `git commit -m "chore(milestone): <description>"`
  - Do not push.
- If it is not a git repository, skip the commit and say so.

## 4. Reply

One short confirmation: the entry appended, whether a roadmap item was checked off, and the commit hash.

## Explicitly out of scope

- Do **not** run any verification commands.
- Do **not** interview the user about the next session.
- Do **not** update the Session Focus, `context.md`, or migrate active backlog tasks.
- Do **not** rotate or archive the changelog.

Those are `/epoch:checkpoint`'s job. Keeping this skill cheap is what makes it get used.
