# Ollama Plugin for Claude Code

This plugin connects Claude Code to a local or remote Ollama instance.

## Config

`~/.claude/ollama.json` — created by `/ollama-setup`:
```json
{ "host": "http://localhost:11434", "model": "llama3.2" }
```

Read in any skill:
```bash
CFG=$(cat ~/.claude/ollama.json 2>/dev/null || echo '{"host":"http://localhost:11434","model":"llama3.2"}')
HOST=$(echo $CFG | jq -r '.host')
MODEL=$(echo $CFG | jq -r '.model')
```

## Environment (set before starting Claude Code)

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434   # or your Ollama host
export ANTHROPIC_AUTH_TOKEN=ollama
```

Run Claude Code against Ollama:
```bash
claude --model llama3.2
```

## Limitations vs Anthropic Claude

- No vision on most models
- No tool use on all models (depends on model)
- Context windows vary by model (check `ollama-status`)
- No streaming guaranteed on all endpoints

## Skills

| Skill | Purpose |
|---|---|
| `/ollama-setup` | Configure host + default model, test connection |
| `/ollama-models` | List installed models |
| `/ollama-pull` | Pull a model from the Ollama library |
| `/ollama-status` | Health check, version, model count |
| `/ollama-switch` | Change active model in config |
