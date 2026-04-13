---
name: ask-ollama
description: Send a prompt to the configured Ollama model and return the response. Use this skill to delegate inference to Ollama instead of Claude.
argument-hint: "<prompt>"
user-invocable: true
tools: Bash
---

# ask-ollama

## Input
`$ARGUMENTS` — the prompt to send. Required.

```bash
if [ ! -f "$HOME/.claude/ollama.json" ]; then
  echo "ERROR: Ollama not configured. Run /ollama-setup first."
  exit 1
fi

HOST=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('host',''))")
MODEL=$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/ollama.json'))); print(d.get('model',''))")

if [ -z "$HOST" ] || [ -z "$MODEL" ]; then
  echo "ERROR: Ollama not configured. Run /ollama-setup first."
  exit 1
fi

PROMPT="$ARGUMENTS"
if [ -z "$PROMPT" ]; then
  echo "Usage: /ask-ollama <prompt>"
  exit 1
fi

PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({'model': sys.argv[1], 'messages': [{'role': 'user', 'content': sys.argv[2]}], 'stream': False}))
" "$MODEL" "$PROMPT")

RESPONSE=$(curl -sf -X POST "$HOST/api/chat" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

if [ -z "$RESPONSE" ]; then
  echo "ERROR: No response from Ollama at $HOST. Is it running?"
  exit 1
fi

echo "$RESPONSE" | python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
content = d.get('message', {}).get('content', '')
model = d.get('model', 'unknown')
if not content:
    print('ERROR: Unexpected response format:')
    print(json.dumps(d, indent=2))
    sys.exit(1)
print(f'[{model}]')
print(content)
"
```
