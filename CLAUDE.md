# Ollama Plugin for Claude Code

Provides skills for managing an Ollama instance and calling Ollama models directly via REST API. Does NOT change the current Claude Code session's LLM provider.

## What the skills do

All skills call the Ollama REST API directly (`curl http://<host>/api/...`). They are independent of whichever LLM provider this Claude Code session is using.

## Config file

`~/.claude/ollama.json` — written by `/ollama-setup`, read by all other skills:
```json
{ "host": "http://localhost:11434", "model": "llama3.2" }
```

Read in a skill:
```bash
CFG=$(cat ~/.claude/ollama.json 2>/dev/null || echo '{"host":"http://localhost:11434","model":"llama3.2"}')
HOST=$(echo $CFG | jq -r '.host')
MODEL=$(echo $CFG | jq -r '.model')
```

## Skills

| Skill | Purpose |
|---|---|
| `/ollama-setup` | Configure host + default model, test connection, write config |
| `/ollama-models` | List installed models with size and date |
| `/ollama-pull` | Pull a model by name |
| `/ollama-status` | Health check — version, model count, running processes |
| `/ollama-switch` | Change active model in config |

## Running a separate Claude Code session against Ollama

To start a *new* terminal session that uses Ollama as the Claude Code provider (separate from this session):

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
claude --model llama3.2
```

This does not affect the current session.
