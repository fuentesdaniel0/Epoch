---
name: checkpoint
description: Execute the Epoch session checkpoint protocol and wrap up the session. Use for /checkpoint, or when the user says "wrap up the session", "save progress", "close out", "let's checkpoint", "commit the state", "I'm done for today", or asks to prepare to close the session.
---

# Session Checkpoint Workflow

When the user triggers `/checkpoint` or asks to prepare to close the session, you must execute the following protocol in exactly this order:

## 1. Status Check
- Run `git status` with `Bash` to see what files have been modified or created during the session.
- Review your recent tool calls and actions to summarize what you accomplished.

## 2. Memory & Tracker Updates
- **Update Active State**: Update `.agents/memory/context.md` to reflect any new architectural changes, active state, or newly established patterns.
- **Task Migration**: Move completed tasks from `.agents/memory/backlog.md` (Active Backlog Tasks) into `.agents/memory/changelog.md`.
- **Chronological History**: Append a brief narrative summary of the session's completed milestones to `.agents/memory/changelog.md`.
- **Memory Rotation & Archiving**: Check the size of `.agents/memory/changelog.md`. If it is growing too long (e.g., tracking more than the last 3 major milestones), automatically move the oldest entries into an archive file (e.g., `.agents/memory/archive/changelog-v1.md`) to preserve context window tokens.

## 3. Next Session Planning
- Interactively ask the user: *"What should our primary focus be for the next session?"* Then **end your turn and wait**; never answer this question yourself.
- Inject their response into the "Session Focus" section at the top of `.agents/memory/backlog.md`.

## 4. Verification (data-driven)
- `Read` the `## Verification Commands` section of `.agents/memory/context.md`.
- If the fenced block lists commands, run each one in order with `Bash` from the repository root and stop at the first failure.
- If the section is absent or the block is empty, state plainly: *"Verification is not configured for this workspace (no commands under `## Verification Commands` in context.md)."* and continue to the next step.
- If any command fails, attempt to fix the issues, or notify the user and ask if they still want to commit.

## 5. Source Control Checkpoint
- Check if the workspace is initialized as a git repository by executing `git rev-parse --is-inside-work-tree` or verifying if a `.git` directory exists.
- If it **is** a git repository:
  - Stage all changes using `git add .`.
  - Commit the changes with a clear, descriptive message summarizing the session's work: `git commit -m "chore(checkpoint): <brief summary of work>"`
  - Do not push unless explicitly requested by the user.
- If it **is not** a git repository:
  - Skip git staging and committing.
  - Advise the user that the workspace is not currently a git repository, and suggest initiating one (`git init`) if they wish to establish version-controlled session states.

## 6. Session Wrap-Up
- Respond to the user with a concise summary of what was accomplished, the verification results, and confirm that the state is committed and the session is ready to be closed. Provide a brief preview of the "Session Focus" that was just established.

## 7. Context Window Reset Reminder
- In your final response, remind the developer about the **Context Window Reset Protocol**:
  - Suggest that if the milestone is fully complete, or if they notice the chat response times slowing down due to a long transcript, they can safely start a fresh Claude Code session (`/clear` or a new `claude` process).
  - Advise them to begin the new session by running `/init`, which reads the memory files under `.agents/memory/` to synchronize state and check current backlog priorities.
