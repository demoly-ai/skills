# Demoly Skills

Official Agent Skills from [Demoly](https://demoly.ai/). Give your AI agent a product URL and get a launch video or a product demo video planned with you, then generated on demoly.ai.

## What the Skills do

| Skill | Use it for |
| --- | --- |
| [`launch-video`](skills/launch-video/SKILL.md) | A narrated launch or promo video built from your product's website: launches, landing pages, social posts. |
| [`product-demo-video`](skills/product-demo-video/SKILL.md) | A narrated walkthrough recorded in your real web app, optionally signed in: feature tours, onboarding, sales demos. |

Your agent reads your product page, drafts the brief with you (audience, what to lead with, which flow to show), and gives you a Demoly link with the product URL and video type already filled in. You paste the brief, pick options, and Demoly makes the video.

Demoly has no agent API yet, so videos are always generated on demoly.ai, under your own account.

## Install

### Claude Code

```text
/plugin marketplace add demoly-ai/skills
/plugin install demoly-skills@demoly-ai
```

### Codex

```bash
codex plugin marketplace add demoly-ai/skills
codex plugin add demoly-skills@demoly-ai
```

### Other agents (Cursor, Gemini CLI, Copilot, Windsurf and more)

With the [Skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add demoly-ai/skills
```

Or copy the folders under `skills/` into your agent's Skills directory, for example `~/.claude/skills/` or `~/.agents/skills/`.

## Just ask

```text
Make a launch video for https://example.com
```

```text
Plan a demo video that shows how a new user sets up their first project in our app.
```

```text
Write the brief for a feature walkthrough of our reporting page.
```

## Privacy and safety

- The Skills never ask for passwords. When a demo needs a signed-in view, you sign in yourself in a live browser on demoly.ai.
- Nothing is sent to Demoly until you submit it on the site. See the [privacy policy](https://demoly.ai/privacy) and [terms](https://demoly.ai/terms).

## Repository

- [Architecture](docs/ARCHITECTURE.md): layout and rules for adding Skills.
- [Roadmap](ROADMAP.md).
- Validate before committing: `python3 scripts/validate_repository.py`.

Licensed under the [MIT License](LICENSE).
