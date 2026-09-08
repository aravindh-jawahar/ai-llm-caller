# 03 · Chat loop

A multi-turn conversation in the terminal. Ask a follow-up question and the
model will answer in context — because we keep and resend the history.

## Run

```bash
uv run python -m examples.chat_loop.main
```

Type your messages at the `you>` prompt. Type `exit` or `quit` (or press
Ctrl-D / Ctrl-C) to stop.

## What to notice

- **The model is stateless.** It only "remembers" earlier turns because we keep
  a `messages` list and send the *whole* list every time.
- Each turn appends **two** messages: the user's, then the assistant's reply.
- The `system` message at the start shapes the assistant's overall behavior for
  the whole conversation.
- Because history grows every turn, real apps eventually need to trim or
  summarize it to stay within the model's context limit — something to explore
  later.
