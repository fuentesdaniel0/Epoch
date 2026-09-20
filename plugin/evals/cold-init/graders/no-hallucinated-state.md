---
type: llm
weight: 2
---

PASS if the reply says this directory was not (yet) an Epoch workspace and that blank memory files were just created, reports the state as blank / uninitialized, and hands off to /epoch:plan (it may also offer a CLAUDE.md snippet and git init as optional extras).
FAIL if the reply describes any concrete tech stack, architecture, tasks, session focus, or history as if it already existed, or if it claims the project is initialized.
