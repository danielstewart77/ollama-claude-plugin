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
CFG=$(cat ~/.claude/ollama.json 2>/dev/null || echo '{"host":"http://localhost:11434","model":"llama3.2"}')
HOST=$(echo $CFG | jq -r '.host')
CURRENT=$(echo $CFG | jq -r '.model')

TARGET="$ARGUMENTS"

if [ -z "$TARGET" ]; then
  MODELS=$(curl -sf "$HOST/api/tags" | jq -r '.models[].name' 2>/dev/null)
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
FOUND=$(curl -sf "$HOST/api/tags" | jq -r ".models[] | select(.name==\"$TARGET\") | .name")
if [ -z "$FOUND" ]; then
  echo "Model '$TARGET' not installed. Run: /ollama-pull $TARGET"
  exit 1
fi

# Write updated config
echo "{\"host\":\"$HOST\",\"model\":\"$TARGET\"}" > ~/.claude/ollama.json
echo "Switched: $CURRENT → $TARGET"
echo "Note: restart Claude Code session to change the underlying model."
```
