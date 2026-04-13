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

if [ ! -f "$HOME/.claude/ollama.json" ]; then
  echo "ERROR: Ollama not configured. Run /ollama-setup first."
  exit 1
fi

HOST=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('host','http://localhost:11434'))")

echo "Pulling $MODEL from $HOST..."
curl -sf -X POST "$HOST/api/pull" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$MODEL\",\"stream\":false}" \
  | python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('status','done'))"

echo "Done. Run /ollama-models to verify."
```

Browse available models: https://ollama.com/library
