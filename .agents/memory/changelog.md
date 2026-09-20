---
protocol_version: 2.0
---

# Project History & Milestone Timeline

This file captures the chronological history of milestones, architectural decisions, and tasks completed in the repository.

---

## Sprint Chronology

### Sprint: Calendar Advisor Agent Integration

* **Accomplishment**: Created a new autonomous agent project (`CalendarAgent/`) under `Dev` based on `CalendarV2`. Ported the parallel availability query execution from `CalendarV2` into `calendar_tools.py` using `gcloud compute advice calendar-mode`. Registered tools in the ADK agent structure for listing machine types, regions, and executing queries. Hardened type validation and test coverage.
* **Decisions**: Extracted file editing/creation tools to keep the advisor agent strictly focused on resource availability.

### Milestone (2026-09-20): Ported Epoch engine to Claude Code

* **Accomplishment**: The rules/workflows engine now exists as native Claude Code constructs (`CLAUDE.md`, `.claude/rules/`, `.claude/skills/`) with new `/init` and `/milestone` skills; `.agents/memory/` is unchanged apart from protocol_version frontmatter and a Verification Commands section.

### Sprint: Claude Code Engine v2 Port

* **Accomplishment**: Rebuilt the Epoch engine as native Claude Code constructs on branch `claude-code-v2`. Added `CLAUDE.md` (Startup SOP, memory map, command index), `.claude/rules/core-directives.md`, and skills `init`, `plan`, `checkpoint`, `milestone`, `scaffold-module` under `.claude/skills/`. Added a `SessionStart` hook in `.claude/settings.json`. Deleted `adk-agent-template/`, `scripts/create-agent.py`, `.agents/{rules,workflows,skills}`, and untracked live MCP configs (sanitized example kept). Replaced the bootstrapper with `scripts/create-workspace.py`, rebuilt `scripts/sync-templates.py` for the new layout (idempotent), added `protocol_version: 2.0` frontmatter and a `## Verification Commands` section to memory files, rewrote `README.md` and `EVALUATION.md` (now six phases including milestone capture), and wired `markdownlint-cli2` as this repo's verification command.
* **Decisions**: State (`.agents/memory/`) stays harness-neutral; only the engine is Claude Code-specific so future adapters stay thin. `/checkpoint` verification is data-driven from `context.md` rather than hardcoded per stack. The project `init` skill intentionally replaces Claude Code's bundled `/init` (documented override behavior). The `SessionStart` hook is kept as belt-and-suspenders alongside `CLAUDE.md`; it omits a matcher so it fires on startup, resume, clear, and compact. Rotated pre-v2 changelog entries into `.agents/memory/archive/changelog-v1.md`.

### Milestone (2026-09-20): Tagged v1.0 and v2.0, merged claude-code-v2 into master
*   **Accomplishment**: Tagged the last Antigravity/ADK commit as `v1.0`, merged `claude-code-v2` into `master` with a no-fast-forward merge commit, and tagged the result `v2.0`. Neither tags nor master have been pushed.
