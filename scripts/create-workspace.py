#!/usr/bin/env python3
"""Epoch workspace bootstrapper.

Copies the pristine `template/` tree into a target directory, runs a short
interview (project name, domain, verification commands), writes the answers
into the new instance's `.agents/memory/context.md`, then initialises git and
makes the first commit.

Usage:
    python3 scripts/create-workspace.py <target-directory> [--name N] [--domain D]
                                        [--verify CMD ...] [--no-git]

Answers can be piped on stdin (one per line) or given as flags; flags win.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys

BANNER = "=" * 60


def ask(prompt: str, default: str = "") -> str:
    """Prompt on stdin. Returns default when the user enters nothing or stdin is closed."""
    suffix = f" [{default}]" if default else ""
    try:
        answer = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        answer = ""
    return answer or default


def ask_commands() -> list[str]:
    """Collect verification commands one per line until a blank line."""
    print("Verification commands (one per line; blank line to finish; leave empty to skip):")
    commands: list[str] = []
    while True:
        try:
            line = input("  $ ").strip()
        except EOFError:
            break
        if not line:
            break
        commands.append(line)
    return commands


def set_frontmatter_key(text: str, key: str, value: str) -> str:
    """Set `key: value` inside the leading YAML frontmatter block, adding it if missing."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return f"---\n{key}: {value}\n---\n\n{text}"
    block = match.group(1)
    pattern = re.compile(rf"^{re.escape(key)}:.*$", re.MULTILINE)
    if pattern.search(block):
        block = pattern.sub(f"{key}: {value}", block)
    else:
        block = f"{block}\n{key}: {value}"
    return f"---\n{block}\n---\n" + text[match.end():]


def set_verification_commands(text: str, commands: list[str]) -> str:
    """Fill the fenced block under `## Verification Commands` with the given commands."""
    if not commands:
        return text
    body = "\n".join(commands)
    pattern = re.compile(r"(## Verification Commands\n(?:.*?\n)*?```bash\n)(.*?)(```)", re.DOTALL)
    if pattern.search(text):
        return pattern.sub(lambda m: f"{m.group(1)}{body}\n{m.group(3)}", text, count=1)
    return text.rstrip("\n") + f"\n\n## Verification Commands\n\n```bash\n{body}\n```\n"


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new Epoch workspace from template/.")
    parser.add_argument("target", help="Directory to create (must not exist or must be empty)")
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--domain", help="One-line description of the project's domain / core goal")
    parser.add_argument("--verify", action="append", metavar="CMD",
                        help="Verification command (repeatable). Overrides the interactive prompt.")
    parser.add_argument("--no-git", action="store_true", help="Skip git init and first commit")
    args = parser.parse_args()

    print(BANNER)
    print("          Epoch Workspace Bootstrapper")
    print(BANNER)

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_dir = os.path.join(root_dir, "template")
    target_dir = os.path.abspath(args.target)

    if not os.path.isdir(template_dir):
        sys.exit(f"Error: template directory not found at {template_dir}")
    if os.path.exists(target_dir) and os.listdir(target_dir):
        sys.exit(f"Error: target directory {target_dir} exists and is not empty.")

    # 1. Copy the pristine template (CLAUDE.md, .claude/, .agents/memory/).
    print(f"\nCopying template into {target_dir} ...")
    shutil.copytree(template_dir, target_dir, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(os.path.join(root_dir, ".gitignore"), os.path.join(target_dir, ".gitignore"))

    # 2. Interview.
    print("\n--- Project Interview ---")
    name = args.name or ask("Project name", os.path.basename(target_dir))
    domain = args.domain or ask("Domain / core goal (one line)", "")
    commands = args.verify if args.verify is not None else ask_commands()

    # 3. Write answers into context.md.
    context_path = os.path.join(target_dir, ".agents", "memory", "context.md")
    with open(context_path, encoding="utf-8") as fh:
        context = fh.read()
    context = set_frontmatter_key(context, "project", quote(name))
    context = set_frontmatter_key(context, "domain", quote(domain))
    context = set_verification_commands(context, commands)
    with open(context_path, "w", encoding="utf-8") as fh:
        fh.write(context)
    print(f"Wrote project details to {os.path.relpath(context_path, target_dir)}")

    # 4. git init + first commit.
    if not args.no_git:
        print("\nInitialising git repository ...")
        try:
            subprocess.run(["git", "init", "-q"], cwd=target_dir, check=True)
            subprocess.run(["git", "add", "-A"], cwd=target_dir, check=True)
            subprocess.run(["git", "commit", "-q", "-m",
                            f"chore(epoch): initialize {name} with Epoch memory protocol v2.1"],
                           cwd=target_dir, check=True)
            print("Initial commit created.")
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            print(f"Warning: git initialisation incomplete ({exc}). "
                  "Check that git is installed and user.name/user.email are configured.")

    print("\n" + BANNER)
    print("          SUCCESS: Epoch workspace created")
    print(BANNER)
    print(f"Path: {target_dir}")
    print("\nNext steps:")
    print(f"  1. cd {args.target}")
    print("  2. claude            # start a Claude Code session")
    print("  3. /init             # read memory state; /plan to fill it in")
    print(BANNER)


if __name__ == "__main__":
    main()
