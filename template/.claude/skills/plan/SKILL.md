---
name: plan
description: Interactive workflow to define a new project or plan the next sprint by reviewing the backlog and migrating tasks. Bootstraps .agents/memory/ in a directory that has none. Use for /epoch:plan or /sprint, or when the user says "let's plan", "set up the project", "groom the backlog", "plan the sprint", "what should we work on next", or "initialize the memory".
---

# Project Planning Workflow

> Invoked as `/epoch:plan` from the Epoch plugin, or `/plan` from a per-repo copy of this skill. The steps are identical.

Workspace memory: !`[ -f .agents/memory/context.md ] && echo present || echo ABSENT`

## 0. Bootstrap check

- If the line above says `present`, skip to step 1. (Per-repo copies of this skill always take this branch.)
- If it says `ABSENT`, this directory is not yet an Epoch workspace. Say so in one sentence, then create the memory from the plugin's bundled templates with `Bash`:

```bash
mkdir -p .agents/memory && cp "${CLAUDE_PLUGIN_ROOT}/templates/memory/"*.md .agents/memory/
```

  If `${CLAUDE_PLUGIN_ROOT}` is not set or the copy fails (this skill is running outside the plugin), stop and tell the user to copy Epoch's `template/.agents/memory/` into `.agents/memory/` instead; do not hand-write memory files.
- Offer, but do not apply unasked, two one-line extras in your next message: (a) append `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.snippet.md` to the project's `CLAUDE.md` (create it if absent); (b) `git init` if `git rev-parse --is-inside-work-tree` fails. Apply whichever the user accepts.
- After a bootstrap the project is uninitialized by definition: go straight into Path A and ask the two extras above together with the interview questions, in one message.

When the user triggers `/epoch:plan` (or `/sprint`), first determine if the project has been initialized: `Read` `.agents/memory/context.md` and check whether it is populated with a project name (frontmatter), a tech stack, and architecture.

Depending on the state, execute one of the following paths interactively.

> **Interview rule for both paths**: when a step says to ask the user, ask, then **end your turn and wait**. Never answer your own interview questions, never assume answers, and never proceed to write memory files until the user has replied.

## Path A: New Project Intake (If not initialized)

### 1. Project Discovery Interview

Ask the user the following questions (you can group them or ask conversationally, but ensure you get answers for all):
- **Project Name & Core Goal**: What is the name of this project and its primary objective?
- **Tech Stack**: What programming languages, frameworks, or tools will we be using?
- **Initial Milestones**: What are the first 1-3 major milestones or features we need to build?
- **Constraints**: Are there any specific architectural constraints, testing requirements, deployment targets, or security considerations?
- **Verification Commands**: Which commands should `/epoch:checkpoint` run to prove the codebase is clean (e.g., `npm test`, `pytest`, `make lint`)? Skip if none exist yet.

*Wait for the user's responses before proceeding to Step 2.*

### 2. Memory Initialization

Once the user provides the details, synthesize the information and update the project tracking templates:
- **`.agents/memory/context.md`**: Set the `project` and `domain` frontmatter keys. Fill out the "Active Stack Details" and basic "Architecture" sections based on the provided tech stack and constraints. Put the verification commands, one per line, inside the fenced block under `## Verification Commands`.
- **`.agents/memory/backlog.md`**: Populate the "High-Level Roadmap" and "Active Backlog Tasks" with the initial milestones discussed. Replace every bracketed placeholder.
- **`.agents/memory/changelog.md`**: Add an entry for "Milestone 0: Project Discovery & Intake" summarizing the established goals.

### 3. Confirmation & Handoff

Present a brief summary of the initialized project state to the user. Confirm that the memory tracking system is now fully tailored to their new project and ready for development. Suggest they provide their first engineering task to get started!

---

## Path B: Sprint Planning (If already initialized)

### 1. Backlog Review

- `Read` `.agents/memory/backlog.md`.
- Present a concise summary of the "Session Focus" (if any) and the top items in the "High-Level Roadmap" to the user.
- Ask the user: *"Which of these roadmap items should we pull into the 'Active Backlog Tasks' for this session? Or is there a new priority not listed here?"*

*Wait for the user's response before proceeding.*

### 2. Queue Grooming & Task Decomposition

Based on the user's response:
- Analyze the selected Roadmap items. If they are large features, **decompose them into atomic, verifiable subtasks**.
- Update `.agents/memory/backlog.md`:
  - Move the selected items (and their subtasks) into the "Active Backlog Tasks".
  - Update the "Session Focus" section to reflect the immediate goal.
- Present the updated "Active Backlog Tasks" queue to the user for confirmation.

### 3. Execution Handoff

- Ask the user: *"Are we ready to begin work on the first task in the queue, or do we need to clarify any architectural details before starting?"*
- Once confirmed, transition smoothly into execution mode, focusing strictly on the first active task.
