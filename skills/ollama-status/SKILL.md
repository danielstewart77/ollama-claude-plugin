---
name: ollama-status
description: Health check for the Ollama server. Reports version, model count, active model, and running processes.
user-invocable: true
tools: Bash
---

# ollama-status

```bash
CFG=$(cat ~/.claude/ollama.json 2>/dev/null || echo '{"host":"http://localhost:11434","model":"llama3.2"}')
HOST=$(echo $CFG | jq -r '.host')
CURRENT=$(echo $CFG | jq -r '.model')

VERSION=$(curl -sf "$HOST/api/version" | jq -r '.version' 2>/dev/null)
if [ -z "$VERSION" ]; then
  echo "OFFLINE — cannot reach Ollama at $HOST"
  echo "Run: ollama serve"
  exit 1
fi

MODEL_COUNT=$(curl -sf "$HOST/api/tags" | jq '.models | length' 2>/dev/null || echo 0)
RUNNING=$(curl -sf "$HOST/api/ps" | jq -r '.models[]?.name' 2>/dev/null || echo "none")

echo "Ollama Status"
echo "============="
echo "Host:          $HOST"
echo "Version:       $VERSION"
echo "Active model:  $CURRENT"
echo "Installed:     $MODEL_COUNT model(s)"
echo "Running:       ${RUNNING:-none}"
```
