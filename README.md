# Ollama Plugin for Claude Code

Run Claude Code against a local or remote [Ollama](https://ollama.com) instance.

## Install

```bash
# Via Claude Code plugin manager
/plugin install danielstewart77/ollama-claude-plugin

# Or manually
git clone https://github.com/danielstewart77/ollama-claude-plugin ~/.claude/plugins/ollama
```

## Quick Start

1. [Install Ollama](https://ollama.com/download) and start it: `ollama serve`
2. Run `/ollama-setup` — configures your host and picks a default model
3. Set env vars (shown by setup) and restart Claude Code

## Skills

| Skill | Description |
|---|---|
| `/ollama-setup` | Configure host URL + default model, test connection |
| `/ollama-models` | List installed models with size and date |
| `/ollama-pull` | Pull a model: `/ollama-pull llama3.2` |
| `/ollama-status` | Health check — version, model count, running processes |
| `/ollama-switch` | Change active model: `/ollama-switch mistral` |

## Config

Written to `~/.claude/ollama.json` by `/ollama-setup`:
```json
{ "host": "http://localhost:11434", "model": "llama3.2" }
```

Edit directly or re-run `/ollama-setup` to change.

## Environment Variables

```bash
export ANTHROPIC_BASE_URL=http://localhost:11434
export ANTHROPIC_AUTH_TOKEN=ollama
claude --model llama3.2
```

## Popular Models

```bash
/ollama-pull llama3.2          # Meta Llama 3.2 (3B)
/ollama-pull llama3.2:latest   # Meta Llama 3.2 (latest)
/ollama-pull mistral           # Mistral 7B
/ollama-pull codellama:13b     # Code Llama 13B
/ollama-pull qwen2.5-coder     # Qwen 2.5 Coder
/ollama-pull nomic-embed-text  # Embeddings model
```

Full library: https://ollama.com/library
