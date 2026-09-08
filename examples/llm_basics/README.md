# 01 · LLM basics

The simplest LLM interaction: send one message, get one reply.

## Run

```bash
uv run python -m examples.llm_basics.main
```

## What to notice

- **`messages`** is a list of `{role, content}` objects. `role` is usually
  `"user"`, `"assistant"`, or `"system"`. Here we send a single user message.
- **`temperature`** controls randomness: `0` is focused/deterministic, higher
  values are more creative. Try changing it and re-running.
- **`response.choices[0].message.content`** is where the reply text lives.

## Note

We use the `chat.completions` API because it works identically across every
provider (NVIDIA, OpenAI, Ollama). NVIDIA also supports the newer `responses`
API (`client.responses.create(...)` with `response.output_text`), but it is not
portable to other providers, so we don't use it here.
