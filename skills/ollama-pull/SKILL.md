---
name: ollama-pull
description: Pull an Ollama model by name. Streams download progress. Run /ollama-models first to see what's already installed.
argument-hint: "<model-name>"
user-invocable: true
tools: Bash
---

# ollama-pull

## Input
`$ARGUMENTS` — model name (e.g. `llama3.2`, `mistral`, `codellama:13b`). Required.

```bash
MODEL="$ARGUMENTS"
if [ -z "$MODEL" ]; then
  echo "Usage: /ollama-pull <model-name>"
  echo "Examples: llama3.2  mistral  codellama:13b  nomic-embed-text"
  exit 1
fi

CFG=$(cat ~/.claude/ollama.json 2>/dev/null || echo '{"host":"http://localhost:11434"}')
HOST=$(echo $CFG | jq -r '.host')

echo "Pulling $MODEL from $HOST..."
curl -sf -X POST "$HOST/api/pull" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$MODEL\",\"stream\":false}" | jq -r '.status'

echo "Done. Run /ollama-models to verify."
```

Browse available models: https://ollama.com/library
