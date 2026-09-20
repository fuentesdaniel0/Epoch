---
protocol_version: 2.0
---

# Product Backlog & Future Tasks

This file outlines the upcoming milestones, roadmap, and individual feature tasks planned for this repository. When an agent completes a task, it should be removed from this list and documented in `changelog.md`.

---

## Session Focus

*This section dictates the immediate priority for the next AI agent session. It is populated during the `/checkpoint` wrap-up or via `/plan`.*

- [ ] v2.1 release: push `plugin-v2.1`, merge to master, tag `v2.1.0`; run the full 3-run eval; submit `plugin/` to the community marketplace via the Console form (owner action).

---

## High-Level Roadmap

### Milestone 1: Template Separation (Completed)

- **Feature 1**: Isolate the pristine template into `template/`.
- **Feature 2**: Re-initialize the root memory to track repository development.

### Milestone 2: Tooling (Completed)

- [x] **Feature 1**: Template sync tool (`scripts/sync-templates.py`) to prevent engine drift.
- [x] **Feature 2**: Interactive workspace bootstrapper (`scripts/create-workspace.py`).

### Milestone 3: Claude Code Engine v2 (Completed)

- [x] **Feature 1**: Port rules/workflows to `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`.
- [x] **Feature 2**: Add `/init` (read-only state report) and `/milestone` (cheap append+commit).
- [x] **Feature 3**: Data-driven `/checkpoint` verification from `## Verification Commands`.
- [x] **Feature 4**: Strip ADK runtime, deployment tooling, and live MCP configs.

### Milestone 4: v2.0 Release (Completed)

- [ ] **Feature 1**: Walk `EVALUATION.md` in a fresh interactive `claude` session (Phases 1-6) and record results.
- [ ] **Feature 2**: Tag `v2.0` and publish release notes.

### Milestone 7: Multi-Harness Adapters (Post v2.1)

- **Feature 1**: Thin engine ports (Cursor, Copilot, Antigravity) over the unchanged `.agents/memory/` state.
- **Feature 2**: Optional domain packs (rules/skills bundles) installable into `.claude/`.

### Continuous Milestone: Meta-Planning & Agent Improvement

- **Feature 1**: Evaluate agent performance across skills and refine `.claude/` constraints.
- **Feature 2**: Ideate new skills or slash commands to augment autonomy.

---

## Active Backlog Tasks

- [ ] Run the full eval suite (default 3 runs, with/without arms) and record the summary table in the changelog.
- [ ] Merge `plugin-v2.1` into master and tag `v2.1.0`.
- [ ] Submit `plugin/` at platform.claude.com/plugins/submit (owner).
