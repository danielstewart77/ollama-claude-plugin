---
name: ollama-setup
description: Configure the Ollama plugin. Prompts for host URL, tests connection, lists models, sets default, writes ~/.claude/ollama.json.
argument-hint: "[host-url]"
user-invocable: true
tools: Bash
---

# ollama-setup

## Inputs
- `$ARGUMENTS` — optional host URL (e.g. `http://192.168.1.x:11434`). If omitted, prompt user.

## Steps

### 1 — Get host
```bash
HOST="${ARGUMENTS:-}"
if [ -z "$HOST" ]; then
  echo "Ollama host URL (e.g. http://192.168.1.x:11434):"
  read INPUT
  if [ -z "$INPUT" ]; then
    echo "ERROR: Host URL is required."
    exit 1
  fi
  HOST="$INPUT"
fi
HOST="${HOST%/}"  # strip trailing slash
```

### 2 — Test connection
```bash
RESP=$(curl -sf "$HOST/api/version")
VERSION=$(echo "$RESP" | python3 -c "import json,sys; print(json.loads(sys.stdin.read()).get('version',''))" 2>/dev/null)
if [ -z "$VERSION" ]; then
  echo "ERROR: Cannot reach Ollama at $HOST"
  echo "Is Ollama running? Try: ollama serve"
  exit 1
fi
echo "Connected — Ollama $VERSION at $HOST"
```

### 3 — List models and pick default
```bash
MODELS=$(curl -sf "$HOST/api/tags" | python3 -c "
import json, sys
data = json.loads(sys.stdin.read())
for m in data.get('models', []):
    print(m['name'])
" 2>/dev/null)
if [ -z "$MODELS" ]; then
  echo "No models installed. Run /ollama-pull to add one."
  DEFAULT_MODEL="llama3.2"
else
  echo "Installed models:"
  echo "$MODELS" | nl
  echo "Enter model name to use as default (or press Enter for first listed):"
  read CHOICE
  DEFAULT_MODEL="${CHOICE:-$(echo "$MODELS" | head -1)}"
fi
```

### 4 — Write config
```bash
python3 -c "
import json, os
cfg = {'host': os.environ['HOST'], 'model': os.environ['DEFAULT_MODEL']}
path = os.path.expanduser('~/.claude/ollama.json')
os.makedirs(os.path.dirname(path), exist_ok=True)
json.dump(cfg, open(path, 'w'))
" HOST="$HOST" DEFAULT_MODEL="$DEFAULT_MODEL"
echo "Config saved — host=$HOST model=$DEFAULT_MODEL"
echo "Run /ollama-status to verify."
```
