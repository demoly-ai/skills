#!/usr/bin/env python3
"""Validate repository-level Agent Skill and plugin invariants. Standard library only."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SHARED_REFERENCES = ["references/demoly-handoff.md"]
SITE_ROUTES = {"/", "/create", "/library", "/contact-us", "/privacy", "/terms", "/login", "/signup"}
SITE_URL = re.compile(r"https://demoly\.ai(/[a-z-]*)?")

errors: list[str] = []


def err(message: str) -> None:
    errors.append(message)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        err(f"{rel(path)} must start with YAML frontmatter")
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if not sep or line.startswith(" "):
            err(f"{rel(path)}: frontmatter must be single-line `key: value` pairs")
            continue
        data[key.strip()] = value.strip()
    return data


def check_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for target in LINK_PATTERN.findall(text):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        local = target.split("#", 1)[0].strip()
        if local and not (path.parent / local).resolve().exists():
            err(f"{rel(path)}: broken local link {target}")
    for match in SITE_URL.finditer(text):
        route = match.group(1) or "/"
        if route not in SITE_ROUTES:
            err(f"{rel(path)}: unknown demoly.ai route {route}")


def check_skill(skill: Path) -> None:
    skill_md = skill / "SKILL.md"
    if not skill_md.is_file():
        err(f"{rel(skill)} is missing SKILL.md")
        return
    meta = frontmatter(skill_md)
    if set(meta) != {"name", "description"}:
        err(f"{rel(skill_md)}: frontmatter must contain only name and description")
    if meta.get("name") != skill.name or not NAME_PATTERN.match(skill.name):
        err(f"{rel(skill_md)}: name must be kebab-case and equal the directory name")
    description = meta.get("description", "")
    if not 50 <= len(description) <= 1024:
        err(f"{rel(skill_md)}: description must be 50-1024 characters")
    if len(skill_md.read_text(encoding="utf-8").splitlines()) > 500:
        err(f"{rel(skill_md)}: keep SKILL.md under 500 lines; move detail to references/")
    agent = skill / "agents" / "openai.yaml"
    if not agent.is_file():
        err(f"{rel(skill)} is missing agents/openai.yaml")
    elif f"${skill.name}" not in agent.read_text(encoding="utf-8"):
        err(f"{rel(agent)}: default_prompt must mention ${skill.name}")
    if not (ROOT / "tests" / skill.name / "cases.md").is_file():
        err(f"tests/{skill.name}/cases.md is missing")
    for name in ("README.md", "CHANGELOG.md"):
        if (skill / name).exists():
            err(f"{rel(skill)}: do not put {name} inside a Skill")
    for md in skill.rglob("*.md"):
        check_links(md)


def check_shared(skills: list[Path]) -> None:
    for ref in SHARED_REFERENCES:
        copies = {s.name: (s / ref).read_text(encoding="utf-8") for s in skills if (s / ref).exists()}
        if len(set(copies.values())) > 1:
            err(f"{ref} differs between Skills {sorted(copies)}; keep the copies identical")


def check_manifests() -> None:
    def load(path: str) -> dict:
        try:
            return json.loads((ROOT / path).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            err(f"{path}: {exc}")
            return {}

    claude = load(".claude-plugin/plugin.json")
    codex = load(".codex-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    agents_market = load(".agents/plugins/marketplace.json")
    entry = next(iter(market.get("plugins", [])), {})
    versions = {claude.get("version"), codex.get("version"), entry.get("version")}
    if len(versions) != 1:
        err(f"plugin versions differ: {sorted(map(str, versions))}")
    names = {claude.get("name"), codex.get("name"), entry.get("name"),
             next(iter(agents_market.get("plugins", [])), {}).get("name")}
    if len(names) != 1:
        err(f"plugin names differ: {sorted(map(str, names))}")
    if codex.get("skills") != "./skills/":
        err(".codex-plugin/plugin.json must expose ./skills/")


def main() -> int:
    if not SKILLS_DIR.is_dir():
        err("missing skills/")
        skills = []
    else:
        skills = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not skills:
        err("the repository must contain at least one Skill")
    for skill in skills:
        check_skill(skill)
    check_shared(skills)
    check_manifests()
    for md in ROOT.glob("*.md"):
        check_links(md)
    for md in (ROOT / "docs").glob("*.md"):
        check_links(md)
    if errors:
        for message in errors:
            print(f"ERROR: {message}", file=sys.stderr)
        return 1
    print(f"OK: {len(skills)} Skills validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
