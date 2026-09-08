# 02 · Streaming

Print the reply token-by-token as the model generates it, instead of waiting
for the whole thing. This is what makes chat UIs feel responsive.

## Run

```bash
uv run python -m examples.streaming.main
```

## What to notice

- The only change from `llm_basics` is **`stream=True`**.
- The return value is now an **iterator of chunks**, not a single response.
- Each chunk's new text is in **`chunk.choices[0].delta.content`** — and it can
  be `None` (e.g. the terminating chunk), so we check before printing.
- `flush=True` forces the terminal to show each piece immediately.
