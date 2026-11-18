# Architecture

## Layout

```text
skills/<skill-name>/
  SKILL.md              # frontmatter: name + description only
  agents/openai.yaml    # Codex display metadata
  references/           # detail loaded on demand
tests/<skill-name>/cases.md   # behavior cases (observable behavior, not wording)
.claude-plugin/         # Claude Code plugin + marketplace (thin, no instructions)
.codex-plugin/          # Codex plugin (thin)
.agents/plugins/        # Codex marketplace
scripts/validate_repository.py
```

Each direct child of `skills/` is one installable Skill. Skills are installed one by one by some clients, so each must stand alone: shared material is copied into every Skill that needs it (currently `references/demoly-handoff.md`), and the validator requires the copies to be identical.

## Rules

1. One Skill per distinct user goal and trigger. Launch videos and product demos have different inputs (marketing page vs. signed-in app) and different safety rules, so they are separate.
2. The Skill is the workflow; demoly.ai is the capability. Until Demoly has an agent API, every Skill ends with a handoff link to `https://demoly.ai/create` (`kind`, `url`, `direction` query parameters). Do not describe tools or APIs that do not exist.
3. Facts in Skills must match the live product: kinds, directions, option names, UI labels, routes. When the product changes, update `references/demoly-handoff.md` in every Skill and the behavior cases.
4. Never invent prices, durations, numbers, or customers. Never handle passwords.
5. Bump the version in all three manifests together for a release (the validator checks they match).
