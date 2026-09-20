# Epoch Protocol Evaluation Script

A manual QA script to verify that Claude Code correctly follows the Epoch memory protocol in a workspace.

Because agents are non-deterministic, you test them behaviorally with the prompts below. Every phase is run in a fresh `claude` session unless stated otherwise.

## Prerequisites

1. The workspace contains `CLAUDE.md`, `.claude/`, and `.agents/memory/` (via `scripts/create-workspace.py` or a copy of `template/`).
2. The workspace is a git repository with a clean working tree.
3. Start a **brand new session**: run `claude` in the workspace root, or `/clear` an existing one.

---

## Phase 1: Startup SOP Test (`CLAUDE.md` + SessionStart hook)

Tests whether Claude executes the Startup SOP without being told to read files.

**Your Prompt:**
> "What is the current state of our project and what is my next task?"

**Expected Behavior:**
- Claude does **not** hallucinate an answer.
- It reads `.agents/memory/context.md` and the Session Focus in `.agents/memory/backlog.md` (visible as `Read` tool calls).
- It answers by quoting the placeholders (if memory is blank) or accurately summarizing the tracked state, and offers `/plan`.

---

## Phase 2: Explicit Initialization Test (`/init`)

Tests the deterministic form of the startup SOP.

**Your Prompt:**
> "/init"

**Expected Behavior:**
- Claude reads all three memory files.
- It reports four sections: architecture snapshot, Session Focus, active backlog tasks, last changelog entry, plus whether verification commands are configured.
- If the memory is blank, it says so and hands off to `/plan` Path A.
- **Crucial**: `git status` shows no modified files afterward. `/init` is read-only.

---

## Phase 3: Workflow Intake Test (`/plan`)

Tests that the interactive skill stops and waits instead of rushing.

**Your Prompt:**
> "/plan"

**Expected Behavior:**
- Claude determines whether the project is initialized.
- It asks the interview questions (Project Name, Tech Stack, Milestones, Constraints, Verification Commands) or asks which roadmap items to pull into the active backlog.
- **Crucial**: Claude ends its turn and waits for your reply. It must not answer its own questions or write memory files before you respond.
- After you answer, it populates `context.md` (including frontmatter `project`/`domain` and `## Verification Commands`), `backlog.md`, and `changelog.md`.

---

## Phase 4: Operational Discipline Test (`.claude/rules/core-directives.md`)

Tests that ambient constraints hold during ordinary work.

**Your Prompt:**
> (Provide dummy answers to the `/plan` interview if it asks.) Then: "Okay, let's create a new math utilities module."

**Expected Behavior:**
- Claude does **not** instantly write a file into a guessed directory.
- It uses `Glob` or `Grep` to inspect the repository structure first.
- It may invoke the `scaffold-module` skill.
- After generating boilerplate it runs a build, lint, or test command with `Bash` (Verification-First Development) before declaring the task complete.

---

## Phase 5: Milestone Capture Test (`/milestone`)

Tests that a milestone is recorded cheaply, without checkpoint ceremony.

**Your Prompt:**
> "/milestone Scaffolded the math utilities module"

**Expected Behavior:**
- Claude appends a dated `### Milestone (YYYY-MM-DD): ...` entry to `changelog.md`.
- It checks off a matching roadmap item in `backlog.md` only if exactly one clearly matches; otherwise it leaves the backlog alone and says so.
- It commits with `chore(milestone): ...` and reports the hash. It does not push.
- **Crucial**: it does **not** run verification commands, does **not** ask about the next session, does **not** touch Session Focus or `context.md`, and does **not** archive the changelog.

---

## Phase 6: State Commitment Test (`/checkpoint`)

Tests the session wrap-up and memory rotation protocol.

**Your Prompt:**
> "/checkpoint"

**Expected Behavior:**
- Claude runs `git status`.
- It updates `context.md`, migrates completed tasks, and appends a sprint summary to `changelog.md`; it archives old entries into `.agents/memory/archive/` if the changelog is long.
- It asks what the focus should be for the **next** session, then stops and waits. Your answer lands in the Session Focus at the top of `backlog.md`.
- It reads `## Verification Commands` from `context.md` and runs them. If the block is empty it says verification is not configured for this workspace and continues.
- It commits with `chore(checkpoint): ...` and does not push.
- It closes with the context-window reset reminder, pointing at `/init` for the next session.

---

## Test Results

If Claude passes all six phases, the memory files and the Claude Code engine are correctly synchronized. If a phase fails, the fix belongs in `template/` (then run `scripts/sync-templates.py`), never only in the live root copy.
