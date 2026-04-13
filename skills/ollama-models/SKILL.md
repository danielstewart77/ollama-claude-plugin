---
name: ollama-models
description: List installed Ollama models with size and modification date. Reads host from ~/.claude/ollama.json.
user-invocable: true
tools: Bash
---

# ollama-models

```bash
if [ ! -f "$HOME/.claude/ollama.json" ]; then
  echo "ERROR: Ollama not configured. Run /ollama-setup first."
  exit 1
fi

HOST=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('host','http://localhost:11434'))")
CURRENT=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('model',''))")

RESULT=$(curl -sf "$HOST/api/tags")
if [ -z "$RESULT" ]; then
  echo "Cannot reach Ollama at $HOST — run /ollama-setup"
  exit 1
fi

echo "Ollama models at $HOST (active: $CURRENT)"
echo "---"
echo "$RESULT" | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
models = data.get('models', [])
if not models:
    print('No models installed.')
else:
    for m in models:
        size_gb = round(m.get('size', 0) / 1073741824, 1)
        modified = m.get('modified_at', '')[:10]
        print(f\"{m['name']:<40} {size_gb}GB  {modified}\")
"
```
