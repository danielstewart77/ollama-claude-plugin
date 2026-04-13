---
name: ollama-status
description: Health check for the Ollama server. Reports version, model count, active model, and running processes.
user-invocable: true
tools: Bash
---

# ollama-status

```bash
if [ ! -f "$HOME/.claude/ollama.json" ]; then
  echo "ERROR: Ollama not configured. Run /ollama-setup first."
  exit 1
fi

HOST=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('host','http://localhost:11434'))")
CURRENT=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('model',''))")

VERSION=$(curl -sf "$HOST/api/version" | python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('version',''))" 2>/dev/null)
if [ -z "$VERSION" ]; then
  echo "OFFLINE — cannot reach Ollama at $HOST"
  echo "Run: ollama serve"
  exit 1
fi

MODEL_COUNT=$(curl -sf "$HOST/api/tags" | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
print(len(data.get('models', [])))
" 2>/dev/null || echo 0)

RUNNING=$(curl -sf "$HOST/api/ps" | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
names = [m['name'] for m in data.get('models', [])]
print('\n'.join(names) if names else 'none')
" 2>/dev/null || echo "none")

echo "Ollama Status"
echo "============="
echo "Host:          $HOST"
echo "Version:       $VERSION"
echo "Active model:  $CURRENT"
echo "Installed:     $MODEL_COUNT model(s)"
echo "Running:       ${RUNNING:-none}"
```
