#!/usr/bin/env python3
"""Sync the pristine Epoch template into this repository's live root instance.

Source of truth: `template/`.
Destinations at the repository root:
  - `CLAUDE.md`            (always overwritten)
  - `.claude/**`           (always overwritten; stale files are NOT deleted)
  - `.agents/memory/**`    (never overwritten: memory files are instance state,
                            only copied when missing at the destination)

Run from anywhere: `python3 scripts/sync-templates.py`. Idempotent.
"""

import filecmp
import os
import shutil

ENGINE_PATHS = ["CLAUDE.md", ".claude"]
MEMORY_PATH = os.path.join(".agents", "memory")


def copy_file(src: str, dst: str) -> bool:
    """Copy src to dst if content differs. Returns True when a write happened."""
    if os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False):
        return False
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    shutil.copy2(src, dst)
    return True


def sync_tree(src: str, dst: str, overwrite: bool) -> int:
    """Recursively copy src into dst. Returns the number of files written."""
    written = 0
    if os.path.isfile(src):
        if overwrite or not os.path.exists(dst):
            written += copy_file(src, dst)
        return written
    for entry in sorted(os.listdir(src)):
        s, d = os.path.join(src, entry), os.path.join(dst, entry)
        if os.path.isdir(s):
            written += sync_tree(s, d, overwrite)
        elif overwrite or not os.path.exists(d):
            written += copy_file(s, d)
    return written


def main() -> None:
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_dir = os.path.join(root_dir, "template")
    if not os.path.isdir(template_dir):
        raise SystemExit(f"Template directory not found: {template_dir}")

    print("Starting template synchronization...")
    print(f"Source of truth: {template_dir}")

    total = 0
    for rel in ENGINE_PATHS:
        src = os.path.join(template_dir, rel)
        if not os.path.exists(src):
            print(f"  skip   {rel} (missing in template)")
            continue
        n = sync_tree(src, os.path.join(root_dir, rel), overwrite=True)
        print(f"  engine {rel}: {n} file(s) written")
        total += n

    mem_src = os.path.join(template_dir, MEMORY_PATH)
    if os.path.isdir(mem_src):
        n = sync_tree(mem_src, os.path.join(root_dir, MEMORY_PATH), overwrite=False)
        print(f"  memory {MEMORY_PATH}: {n} missing file(s) created (existing never overwritten)")
        total += n

    print(f"Template synchronization complete: {total} file(s) written.")


if __name__ == "__main__":
    main()
