
## Epoch memory protocol

This project uses the Epoch plugin for persistent state. State lives in `.agents/memory/` (`context.md`, `backlog.md`, `changelog.md`).
On every new session, silently read `context.md` and the Session Focus at the top of `backlog.md` before answering anything about project state.
Commands: `/epoch:init` (read-only state report), `/epoch:plan` (intake or sprint planning), `/epoch:milestone <text>` (append + commit), `/epoch:checkpoint` (full wrap-up, never pushes).
