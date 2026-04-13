---
name: ollama-models
description: List installed Ollama models with size and modification date. Reads host from ~/.claude/ollama.json.
user-invocable: true
tools: Bash
---

# ollama-models

```bash
CFG=$(cat ~/.claude/ollama.json 2>/dev/null || echo '{"host":"http://localhost:11434","model":"llama3.2"}')
HOST=$(echo $CFG | jq -r '.host')
CURRENT=$(echo $CFG | jq -r '.model')

RESULT=$(curl -sf "$HOST/api/tags")
if [ -z "$RESULT" ]; then
  echo "Cannot reach Ollama at $HOST — run /ollama-setup"
  exit 1
fi

echo "Ollama models at $HOST (active: $CURRENT)"
echo "---"
echo "$RESULT" | jq -r '.models[] | "\(.name)\t\(.size / 1073741824 | . * 10 | round / 10)GB\t\(.modified_at[:10])"' \
  | column -t -s $'\t'
```
