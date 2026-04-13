---
name: ollama-switch
description: Change the active Ollama model in ~/.claude/ollama.json. Lists installed models and prompts for selection.
argument-hint: "[model-name]"
user-invocable: true
tools: Bash
---

# ollama-switch

## Input
`$ARGUMENTS` — model name. If omitted, lists installed models and prompts.

```bash
if [ ! -f "$HOME/.claude/ollama.json" ]; then
  echo "ERROR: Ollama not configured. Run /ollama-setup first."
  exit 1
fi

HOST=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('host','http://localhost:11434'))")
CURRENT=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('model',''))")

TARGET="$ARGUMENTS"

if [ -z "$TARGET" ]; then
  MODELS=$(curl -sf "$HOST/api/tags" | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
for m in data.get('models', []):
    print(m['name'])
" 2>/dev/null)
  if [ -z "$MODELS" ]; then
    echo "No models installed. Run /ollama-pull <model-name> first."
    exit 1
  fi
  echo "Installed models (current: $CURRENT):"
  echo "$MODELS" | nl
  echo "Enter model name:"
  read TARGET
fi

# Verify model exists
FOUND=$(curl -sf "$HOST/api/tags" | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
target = sys.argv[1]
found = next((m['name'] for m in data.get('models', []) if m['name'] == target), '')
print(found)
" "$TARGET")

if [ -z "$FOUND" ]; then
  echo "Model '$TARGET' not installed. Run: /ollama-pull $TARGET"
  exit 1
fi

# Write updated config
python3 -c "
import json, os
cfg = {'host': os.environ['HOST'], 'model': os.environ['TARGET']}
json.dump(cfg, open(os.path.expanduser('~/.claude/ollama.json'), 'w'))
" HOST="$HOST" TARGET="$TARGET"
echo "Switched: $CURRENT → $TARGET"
echo "Note: restart Claude Code session to change the underlying model."
```
