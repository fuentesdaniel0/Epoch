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

## Requirements and status

Bash grants require Claude Code's sandbox backend (`bubblewrap` + `socat` on Linux); without it the runner refuses the run. Last recorded run (2026-09-20, `--runs 1`): `state-restoration` passed at 1.0 (0.6 without the plugin). The three Bash-dependent cases are pending an environment with `socat`; their behaviors were verified manually with `claude -p --plugin-dir ./plugin` on the same fixtures.
