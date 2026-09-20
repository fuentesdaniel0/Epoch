# Core Agentic Directives

When operating within this repository, all AI agents must adhere to these foundational behaviors regardless of the active tech stack:

## 1. Active Exploration

- **Do not guess file structures or hallucinate paths.** Always use `Glob` or `Grep` to actively locate the correct modules and configuration files before executing modifications.
- **Context Minimization**: Only use `Read` on files directly relevant to your immediate subtask to preserve token efficiency.

## 2. Verification-First Development

- **Continuous Validation**: Do not wait for the final `/checkpoint` skill to verify your code. Run the appropriate build commands, type checkers (e.g., `npx tsc`), or test suites with `Bash` immediately after completing a logical chunk of work. The project's canonical commands are listed under `## Verification Commands` in `.agents/memory/context.md`.
- **Proof of Success**: Provide the developer with concrete proof (e.g., test output logs or build success messages) before declaring a task completed.

## 3. Atomic Decompositions

- Never attempt to implement large, complex features in a single monolithic edit. Break problems down into small, verifiable steps.
