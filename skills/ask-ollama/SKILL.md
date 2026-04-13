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
CFG=$(cat ~/.claude/ollama.json 2>/dev/null || echo '{}')
HOST=$(echo "$CFG" | jq -r '.host // empty')
MODEL=$(echo "$CFG" | jq -r '.model // empty')

if [ -z "$HOST" ] || [ -z "$MODEL" ]; then
  echo "ERROR: Ollama not configured. Run /ollama-setup first."
  exit 1
fi

PROMPT="$ARGUMENTS"
if [ -z "$PROMPT" ]; then
  echo "Usage: /ask-ollama <prompt>"
  exit 1
fi

PAYLOAD=$(jq -n --arg model "$MODEL" --arg content "$PROMPT" \
  '{"model":$model,"messages":[{"role":"user","content":$content}],"stream":false}')

RESPONSE=$(curl -sf -X POST "$HOST/api/chat" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

if [ -z "$RESPONSE" ]; then
  echo "ERROR: No response from Ollama at $HOST. Is it running?"
  exit 1
fi

CONTENT=$(echo "$RESPONSE" | jq -r '.message.content // empty')
if [ -z "$CONTENT" ]; then
  echo "ERROR: Unexpected response format:"
  echo "$RESPONSE"
  exit 1
fi

echo "[$MODEL]"
echo "$CONTENT"
```
