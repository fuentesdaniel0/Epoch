# Active State & Current Architecture

This file documents the active state, current configurations, code graph, and verification status of the current project.

> [!IMPORTANT]
> **Concision Constraint**: Keep all entries in this file extremely concise. Prune deprecated modules or obsolete state immediately to preserve token space.

---

## Active Stack Details

| Layer | Technology | Key Details |
| :--- | :--- | :--- |
| **Framework** | Markdown protocol | Files under `.agents/memory/` are the whole runtime state |
| **Language/Typing** | Markdown, Python 3 | Python only for `scripts/` tooling |
| **Testing** | Behavioral (`EVALUATION.md`) | Manual QA script walked against a fresh session |
| **Deployment** | None | Distributed by copying `template/` |

---

## Architecture / Code Graph

*Describe the high-level architecture or monorepo structure here.*

```mermaid
graph TD
    Root["/"]
    Template["template/.agents/"]
    RootAgents[".agents/"]
    Eval["EVALUATION.md"]
    Root --> Template
    Root --> RootAgents
    Root --> Eval
```

### Module Descriptions:
- **`template/.agents/`**: The pristine distribution folder containing rules, skills, and blank memory templates.
- **`.agents/`**: The active memory system tracking the development of *this* repository itself.
- **`EVALUATION.md`**: Behavioral test script for verifying AI agent compliance.

---

## Environment / Security Notes

*   No secrets or cloud resources. Live harness config files (`.agents/settings.json`, `.agents/mcp_config.json`) are git-ignored; see `.agents/mcp_config.example.json`.

---

## Verification Compliance Status

We enforce strict validation criteria. The current status is:

1.  **Type Checks**: N/A
2.  **Linting**: Clean Markdown.
3.  **Test Suites**: N/A (behavioral evaluation only)
4.  **Production Builds**: N/A
