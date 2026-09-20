# Epoch Protocol Evaluation Script

A manual QA script to verify that Claude Code correctly follows the Epoch memory protocol in a workspace.

Because agents are non-deterministic, you test them behaviorally with the prompts below. Every phase is run in a fresh `claude` session unless stated otherwise.

Commands are shown in their plugin form (`/epoch:init`, `/epoch:plan`, `/epoch:milestone`, `/epoch:checkpoint`). Per-repo copies made from `template/` answer to the un-prefixed forms (`/init`, `/plan`, ...). Behavior is identical.

## Prerequisites

1. The `epoch` plugin is installed (`/plugin install epoch@epoch`) or loaded with `claude --plugin-dir ./plugin`; or the workspace contains a per-repo copy of `template/` (`scripts/create-workspace.py` or `cp`).
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
- It answers by quoting the placeholders (if memory is blank) or accurately summarizing the tracked state, and offers `/epoch:plan`.

---

## Phase 2: Explicit Initialization Test (`/epoch:init`)

Tests the deterministic form of the startup SOP.

**Your Prompt:**
> "/epoch:init"

**Expected Behavior:**
- Claude reads all three memory files.
- It reports four sections: architecture snapshot, Session Focus, active backlog tasks, last changelog entry, plus whether verification commands are configured.
- If the memory is blank, it says so and hands off to `/epoch:plan` Path A.
- **Crucial**: `git status` shows no modified files afterward. `/epoch:init` is read-only.

---

## Phase 3: Workflow Intake Test (`/epoch:plan`)

Tests that the interactive skill stops and waits instead of rushing.

**Your Prompt:**
> "/epoch:plan"

**Expected Behavior:**
- Claude determines whether the project is initialized.
- It asks the interview questions (Project Name, Tech Stack, Milestones, Constraints, Verification Commands) or asks which roadmap items to pull into the active backlog.
- **Crucial**: Claude ends its turn and waits for your reply. It must not answer its own questions or write memory files before you respond.
- After you answer, it populates `context.md` (including frontmatter `project`/`domain` and `## Verification Commands`), `backlog.md`, and `changelog.md`.

---

## Phase 4: Operational Discipline Test (`.claude/rules/core-directives.md`)

Tests that ambient constraints hold during ordinary work.

**Your Prompt:**
> (Provide dummy answers to the `/epoch:plan` interview if it asks.) Then: "Okay, let's create a new math utilities module."

**Expected Behavior:**
- Claude does **not** instantly write a file into a guessed directory.
- It uses `Glob` or `Grep` to inspect the repository structure first.
- It may invoke the `scaffold-module` skill.
- After generating boilerplate it runs a build, lint, or test command with `Bash` (Verification-First Development) before declaring the task complete.

---

## Phase 5: Milestone Capture Test (`/epoch:milestone`)

Tests that a milestone is recorded cheaply, without checkpoint ceremony.

**Your Prompt:**
> "/epoch:milestone Scaffolded the math utilities module"

**Expected Behavior:**
- Claude appends a dated `### Milestone (YYYY-MM-DD): ...` entry to `changelog.md`.
- It checks off a matching roadmap item in `backlog.md` only if exactly one clearly matches; otherwise it leaves the backlog alone and says so.
- It commits with `chore(milestone): ...` and reports the hash. It does not push.
- **Crucial**: it does **not** run verification commands, does **not** ask about the next session, does **not** touch Session Focus or `context.md`, and does **not** archive the changelog.

---

## Phase 6: State Commitment Test (`/epoch:checkpoint`)

Tests the session wrap-up and memory rotation protocol.

**Your Prompt:**
> "/epoch:checkpoint"

**Expected Behavior:**
- Claude runs `git status`.
- It updates `context.md`, migrates completed tasks, and appends a sprint summary to `changelog.md`; it archives old entries into `.agents/memory/archive/` if the changelog is long.
- It asks what the focus should be for the **next** session, then stops and waits. Your answer lands in the Session Focus at the top of `backlog.md`.
- It reads `## Verification Commands` from `context.md` and runs them. If the block is empty it says verification is not configured for this workspace and continues.
- It commits with `chore(checkpoint): ...` and does not push.
- It closes with the context-window reset reminder, pointing at `/epoch:init` for the next session.

---

## Phase 7: Fresh-machine plugin flow (`/plugin install` + self-bootstrap)

Tests the primary installation path end-to-end on a machine that has never seen Epoch.

**Steps:**

1. In Claude Code: `/plugin marketplace add fuentesdaniel0/Epoch` then `/plugin install epoch@epoch` (or `claude --plugin-dir ./plugin` from this repo for local testing).
2. Create an empty directory, `cd` into it, start `claude`.
3. Prompt: `/epoch:plan`.
4. Answer the interview. Accept the `git init` extra; accept or decline the `CLAUDE.md` snippet.
5. Do a small task, then `/epoch:milestone "first task"`, then `/epoch:checkpoint`.
6. Start a fresh session in the same directory and ask: "What is the current state of the project?"

**Expected Behavior:**
- Step 3: Claude says the directory is not yet an Epoch workspace, creates `.agents/memory/` with the three blank files, offers the two extras, and asks the Path A interview questions in the same message, then stops and waits.
- Step 4: memory files are populated from your answers; the git repo exists if accepted.
- Step 5: milestone appends and commits without verification; checkpoint runs the full protocol and commits.
- Step 6: the `SessionStart` hook has injected the Startup SOP; Claude reads memory and answers from it. In a directory without `.agents/memory/`, the hook is silent.
- `/epoch:checkpoint` or `/epoch:milestone` in a directory with no memory refuse and point to `/epoch:plan`.

---

## Test Results

If Claude passes all seven phases, the memory files and the Claude Code engine are correctly synchronized. If a phase fails, the fix belongs in `template/` (then run `scripts/sync-templates.py`), never only in the live root copy.
