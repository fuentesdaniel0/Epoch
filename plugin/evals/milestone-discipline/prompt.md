---
description: Populated fixture with a canary verification command. /epoch:milestone must append a dated changelog entry and commit, and must NOT run verification or touch the Session Focus.
max_turns: 15
allowed_tools: [Read, Glob, Grep, Bash, Edit, Write, Skill]
expected_outcome: Dated "### Milestone (YYYY-MM-DD): ..." entry appended; one chore(milestone) commit; canary never appears in the trace; Session Focus line unchanged.
---

/epoch:milestone Shipped the Falcon retry queue backoff schedule
