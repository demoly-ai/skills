# Roadmap

## Available (0.1.0)

- `launch-video`, `product-demo-video`: plan the brief in the agent, hand off to demoly.ai with a prefilled link.

## Next

- Prefill the brief through the link (needs a `prompt` query parameter on `/create`), so the user no longer pastes it.
- Agent API and MCP server: create a video, check its progress, and fetch the download link from the agent, authenticated with a per-user API key. Needs API keys, quotas or billing, and rate limits on the Demoly side first. Adds a `setup-demoly` Skill for connecting.

## Candidates

- `product-video-script`: write a scene-by-scene script for a product video without generating it.
- Video variants from a finished Demoly video: social cut-downs, captions in other languages.
