---
description: "Empty directory. /epoch:init must bootstrap blank memory from the plugin templates and must not invent project state."
max_turns: 15
allowed_tools: [Read, Glob, Grep, Bash, Write, Skill]
expected_outcome: "Memory directory created from templates; reply says the workspace was just bootstrapped and is blank, and hands off to /epoch:plan."
---

/epoch:init
