# Ollama Plugin for Claude Code

Provides skills for managing an Ollama instance and calling Ollama models directly via REST API. Does not affect the current Claude Code session's LLM provider or any environment variables.

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
| `/ask-ollama` | Send a prompt to the configured model, return its response. Use this to delegate inference to Ollama from any skill or workflow step. |
| `/ollama-setup` | Configure host + default model, test connection, write config |
| `/ollama-models` | List installed models with size and date |
| `/ollama-pull` | Pull a model by name |
| `/ollama-status` | Health check — version, model count, running processes |
| `/ollama-switch` | Change active model in config |
| `/ollama-update` | Pull latest version from GitHub, update install record, remove stale cache |

## Delegation pattern

To route inference through Ollama in a skill, invoke `/ask-ollama` as a step:
```
Step N — Generate summary
Invoke /ask-ollama with the collected data as the prompt. Use its response as the output.
```

To mark an entire skill as Ollama-only, add to the skill description:
```
All inference steps use /ask-ollama — do not use Claude for generation.
```
