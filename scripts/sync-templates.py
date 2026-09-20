#!/usr/bin/env python3
"""Propagate the Epoch engine from its single source of truth to every copy.

Source of truth:
  plugin/skills/            -> the engine (SKILL.md files)
  plugin/templates/memory/  -> blank state templates
  template/CLAUDE.md, template/.claude/rules/, template/.claude/settings.json
                            -> hand-maintained pieces of the copy-a-folder path
                               (not part of the plugin, which ships its own hook)

Destinations:
  template/.claude/skills/        (generated, always overwritten, stale skills removed)
  template/.agents/memory/        (generated, always overwritten)
  <root>/CLAUDE.md                (from template/, always overwritten)
  <root>/.claude/rules|settings   (from template/, always overwritten)
  <root>/.claude/skills/          (from plugin/skills, always overwritten, stale removed)
  <root>/.agents/memory/          (from plugin/templates/memory, NEVER overwritten:
                                   only files missing at the destination are created)

Run from anywhere: `python3 scripts/sync-templates.py`. Idempotent.
"""

import filecmp
import os
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PLUGIN_SKILLS = os.path.join(ROOT, "plugin", "skills")
PLUGIN_MEMORY = os.path.join(ROOT, "plugin", "templates", "memory")
TEMPLATE = os.path.join(ROOT, "template")


def copy_file(src: str, dst: str) -> bool:
    if os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False):
        return False
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    shutil.copy2(src, dst)
    return True


def sync_tree(src: str, dst: str, overwrite: bool, prune: bool = False) -> tuple[int, int]:
    """Mirror src into dst. Returns (files written, files removed)."""
    written = removed = 0
    if os.path.isfile(src):
        if overwrite or not os.path.exists(dst):
            written += copy_file(src, dst)
        return written, removed
    os.makedirs(dst, exist_ok=True)
    src_entries = set(os.listdir(src))
    for entry in sorted(src_entries):
        s, d = os.path.join(src, entry), os.path.join(dst, entry)
        if os.path.isdir(s):
            w, r = sync_tree(s, d, overwrite, prune)
            written += w
            removed += r
        elif overwrite or not os.path.exists(d):
            written += copy_file(s, d)
    if prune:
        for entry in sorted(set(os.listdir(dst)) - src_entries):
            target = os.path.join(dst, entry)
            shutil.rmtree(target) if os.path.isdir(target) else os.remove(target)
            removed += 1
    return written, removed


def report(label: str, result: tuple[int, int]) -> None:
    w, r = result
    print(f"  {label}: {w} written, {r} removed")


def main() -> None:
    for required in (PLUGIN_SKILLS, PLUGIN_MEMORY, TEMPLATE):
        if not os.path.isdir(required):
            raise SystemExit(f"Missing source directory: {required}")

    print("Epoch sync: plugin/ -> template/ -> repo root")

    # 1. plugin -> template (generated copy-a-folder distribution)
    report("template/.claude/skills",
           sync_tree(PLUGIN_SKILLS, os.path.join(TEMPLATE, ".claude", "skills"), overwrite=True, prune=True))
    report("template/.agents/memory",
           sync_tree(PLUGIN_MEMORY, os.path.join(TEMPLATE, ".agents", "memory"), overwrite=True, prune=True))

    # 2. template -> root engine (dogfood instance)
    for rel in ("CLAUDE.md", os.path.join(".claude", "rules"), os.path.join(".claude", "settings.json")):
        src = os.path.join(TEMPLATE, rel)
        if os.path.exists(src):
            report(rel, sync_tree(src, os.path.join(ROOT, rel), overwrite=True, prune=os.path.isdir(src)))
    report(".claude/skills",
           sync_tree(PLUGIN_SKILLS, os.path.join(ROOT, ".claude", "skills"), overwrite=True, prune=True))

    # 3. plugin -> root memory (state: never overwrite what exists)
    report(".agents/memory (missing only)",
           sync_tree(PLUGIN_MEMORY, os.path.join(ROOT, ".agents", "memory"), overwrite=False))

    print("Done.")


if __name__ == "__main__":
    main()
