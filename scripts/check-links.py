#!/usr/bin/env python3
"""Check internal links and skill naming across the pack.

Three checks, because all three have broken silently before:

1. Every relative markdown link resolves to a file that exists.
2. Every skills/<dir>/SKILL.md has a `name:` matching its directory, which is what
   makes the skill discoverable once it is copied flat into ~/.claude/skills/.
3. Skills are exactly one level deep. `cp -R ./skills/* ~/.claude/skills/` copies
   directories as they are, so a nested skill would arrive as a folder with no
   SKILL.md in it and would never be found.

Usage:  python scripts/check-links.py [--quiet]
Exit code 1 if anything fails, so it can run in CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}

# [text](target) but not ![image](...) handled the same way, both must resolve.
LINK = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+?)\s*(?:\"[^\"]*\")?\)")
NAME_LINE = re.compile(r"^name:\s*(\S+)\s*$", re.MULTILINE)

EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "//")


def md_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def check_links() -> list[str]:
    problems = []
    for path in md_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for raw in LINK.findall(text):
            target = raw.strip()
            if target.startswith(EXTERNAL_PREFIXES) or target.startswith("#"):
                continue
            # Root-relative targets are paths on the user's own website, not paths
            # in this repo. They appear in example copy inside the skills.
            if target.startswith("/"):
                continue
            # Strip any fragment, then percent-decode.
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel = path.relative_to(ROOT).as_posix()
                problems.append(f"broken link: {rel} -> {raw}")
    return problems


def check_skill_names() -> list[str]:
    problems = []
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        return ["missing skills/ directory"]
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"no SKILL.md: skills/{child.name}/")
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        match = NAME_LINE.search(text)
        if not match:
            problems.append(f"no name: in frontmatter: skills/{child.name}/SKILL.md")
        elif match.group(1) != child.name:
            problems.append(
                f"name mismatch: skills/{child.name}/SKILL.md says "
                f"name: {match.group(1)}"
            )
        # Check 3: a nested skill would not survive a flat copy.
        for grandchild in child.iterdir():
            if grandchild.is_dir() and (grandchild / "SKILL.md").is_file():
                problems.append(
                    f"nested skill would not be discovered: "
                    f"skills/{child.name}/{grandchild.name}/SKILL.md"
                )
    return problems


def main() -> int:
    quiet = "--quiet" in sys.argv
    link_problems = check_links()
    name_problems = check_skill_names()
    problems = link_problems + name_problems

    if not quiet:
        print(f"checked {len(md_files())} markdown files")
        skills = [p for p in (ROOT / 'skills').iterdir() if p.is_dir()] if (ROOT / "skills").is_dir() else []
        print(f"checked {len(skills)} skills")

    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1

    if not quiet:
        print("all links resolve, all skill names match their directories")
    return 0


if __name__ == "__main__":
    sys.exit(main())
