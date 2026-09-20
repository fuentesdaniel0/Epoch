# Epoch plugin eval suite

Four behavioral cases for `claude plugin eval`. Fixtures are created by each case's `fixture.sh` (needs `--scaffold`); skills that write files need an operator tool grant.

| Case | Checks |
| :--- | :--- |
| `cold-init` | Empty dir + `/epoch:init` creates memory from the bundled templates and reports blank state, no invention. |
| `state-restoration` | Populated memory + "what is the state?" answers from `context.md`/`backlog.md` (fixture Session Focus string). |
| `milestone-discipline` | `/epoch:milestone` appends a dated entry and commits; the verification canary never runs; Session Focus untouched. |
| `checkpoint-verification` | A failing Verification Command makes `/epoch:checkpoint` surface the failure and stop, with no commit. |

Pre-release gate, from the repo root:

```bash
claude plugin eval ./plugin --scaffold --allow-tools Bash Write Edit --trust-plugin --no-publish
```

Add `--runs 1 --ablation none -j 4` for a fast smoke pass. Results land in `plugin/evals/results/` (git-ignored).

## Last recorded run

2026-09-20, default settings (3 runs per arm, with/without baseline), Claude Code 2.1.278:

| Case | WITH | W/OUT | Δ |
| :--- | :--- | :--- | :--- |
| cold-init | 1.00 | 0.00 | +1.00 |
| milestone-discipline | 1.00 | 0.50 | +0.50 |
| checkpoint-verification | 1.00 | 0.62 | +0.38 |
| state-restoration | 1.00 | 1.00 | 0.00 |

All four pass at threshold 1.0. `state-restoration` does not discriminate: without the plugin Claude still reads the memory files when they are the only documentation, which is the intended fallback.

## Requirements

Granting `Bash` requires Claude Code's sandbox backend. On Linux that means `bubblewrap` and `socat`:

```bash
sudo apt install bubblewrap socat
```

Without them the runner refuses the run rather than executing unconfined.

## Writing cases for this plugin

Two lessons from building this suite, worth keeping:

- **Fixtures must be self-consistent.** Claude checks the working tree against the memory files. A fixture whose `context.md` describes a FastAPI service must actually contain one, and a milestone case must contain the work it claims shipped. Otherwise Claude correctly refuses to record or report state it cannot corroborate, and the case fails for the right reason at the wrong layer.
- **`tool_used: Skill` does not fire for slash invocations.** A prompt of `/epoch:init` expands the skill into the prompt rather than dispatching a `Skill` tool call, so that grader can never pass. Grade the skill's effects instead.

Grader paths are plain globs; brace alternation such as `{backlog,changelog}.md` does not match.
