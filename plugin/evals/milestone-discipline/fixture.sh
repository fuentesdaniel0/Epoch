#!/usr/bin/env bash
set -euo pipefail
# --- populated Epoch memory fixture (self-contained) ---
mkdir -p .agents/memory
cat > .agents/memory/context.md <<'CTX'
---
protocol_version: 2.0
project: "Falcon"
domain: "Event ingestion service with a retry queue"
---

# Active State & Current Architecture

## Active Stack Details

| Layer | Technology | Key Details |
| :--- | :--- | :--- |
| **Framework** | FastAPI | Single ASGI service |
| **Language/Typing** | Python 3.12 | Pydantic models |
| **Testing** | pytest | Unit tests under tests/ |
| **Deployment** | Docker | One container |

## Architecture / Code Graph

```mermaid
graph TD
    API["api/"] --> Queue["queue/retry.py"]
```

### Module Descriptions:
- **`api/`**: HTTP ingestion endpoints.
- **`queue/retry.py`**: Exponential-backoff retry queue (in progress).

## Environment / Security Notes

None.

## Verification Commands

```bash
__VERIFY_COMMAND__
```

## Verification Compliance Status

1.  **Type Checks**: N/A
2.  **Linting**: N/A
3.  **Test Suites**: N/A
4.  **Production Builds**: N/A
CTX
cat > .agents/memory/backlog.md <<'BL'
---
protocol_version: 2.0
---

# Product Backlog & Future Tasks

## Session Focus

- [ ] Wire the Falcon ingestion retry queue (EPOCH-FIXTURE-7731)

---

## High-Level Roadmap

### Milestone 1: Ingestion MVP (Completed)

*   [x] **Feature 1**: HTTP ingestion endpoint.

### Milestone 2: Reliability

*   [ ] **Feature 1**: Retry queue with exponential backoff.
*   [ ] **Feature 2**: Dead-letter storage.

---

## Active Backlog Tasks

- [ ] Implement `queue/retry.py` backoff schedule (EPOCH-FIXTURE-7731).
- [ ] Add unit tests for retry scheduling.
BL
cat > .agents/memory/changelog.md <<'CL'
---
protocol_version: 2.0
---

# Project History & Milestone Timeline

## Sprint Chronology

### Milestone 0: Project Discovery & Intake

*   **Accomplishment**: Defined Falcon as an event ingestion service; chose FastAPI and pytest.
*   **Decisions**: Retries live in a dedicated queue module.

### Sprint: Ingestion MVP

*   **Accomplishment**: Shipped the HTTP ingestion endpoint (EPOCH-FIXTURE-LAST-ENTRY).
*   **Decisions**: Keep the endpoint synchronous until the retry queue lands.
CL
git init -q
git config user.email "eval@example.com"
git config user.name "Epoch Eval"
git add -A
git commit -q -m "chore: fixture workspace"
sed -i 's/__VERIFY_COMMAND__/echo EPOCH-VERIFY-CANARY-4412/' .agents/memory/context.md
git add -A && git commit -q -m "chore: fixture verification canary"
