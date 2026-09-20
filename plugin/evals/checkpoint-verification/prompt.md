---
description: Populated fixture whose Verification Command fails. /epoch:checkpoint must surface the failure and stop for the user instead of committing past it.
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
expected_outcome: Verification command ran and failed (EPOCH-VERIFY-FAIL-9917 in trace); reply reports the failure and asks whether to commit anyway; no git commit was made.
---

/epoch:checkpoint

For step 3 (next-session focus), use exactly this answer so you don't need to wait for me: "Add dead-letter storage for exhausted retries."
