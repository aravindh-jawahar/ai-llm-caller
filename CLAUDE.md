# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

A learning playground that demonstrates AI techniques one topic at a time —
starting with LLM integration and expanding toward RAG, LangChain, agents, etc.
The guiding principle is **"rewind"**: each topic must be understandable in
isolation weeks later. So every topic is a self-contained module, and shared
setup is confined to a small, stable `core/`.

## Architecture

- **`core/`** — shared plumbing only (config + client). Small and stable.
  - `core/config.py` — reads `.env` into a `Settings` dataclass (`AI_PROVIDER`, optional `AI_MODEL`).
  - `core/providers.py` — a `PROVIDERS` registry mapping a provider name to
    `(base_url, key_env, default_model)`, plus `get_client()` which returns a
    configured `openai.OpenAI` client. NVIDIA, OpenAI, and Ollama are all
    OpenAI-compatible, so the abstraction is thin: switching providers = change
    `AI_PROVIDER` in `.env`; adding one = add a `PROVIDERS` entry.
- **`examples/<topic>/`** — one folder per topic, each with `main.py`
  (exposing `run()` + a `python -m` entry point) and a `README.md`.
  **AI logic lives here, never in `core/`.** Currently: `llm_basics`,
  `streaming`, `chat_loop`, `structured_output`, `data_model_and_validations`
  (the last has a `topics/` subpackage: 10 runnable Pydantic v2 validation
  lessons + a `run_all` runner).
- **`main.py`** — a menu that lists examples and runs the chosen one.
- **`tests/`** — unit tests for `core` logic only; **no network calls**. Live
  API calls are exercised manually by running the examples.

Examples use the **`chat.completions`** API (universal across all providers),
not NVIDIA's provider-specific `responses` API.

## Environment & tooling

- **Package manager:** [`uv`](https://docs.astral.sh/uv/) (`uv.lock` present — do not hand-edit).
- **Python:** 3.13+ (`requires-python = ">=3.13"`, pinned via `.python-version`).
- **Config:** copy `.env.example` to `.env` and set `AI_PROVIDER` + the matching
  API key. `.env` is gitignored; never hardcode keys in source.

## Common commands

```bash
uv sync                                        # sync the virtualenv from the lockfile
uv run main.py                                 # interactive menu
uv run python -m examples.llm_basics.main      # run one example directly
uv run pytest                                  # run all tests
uv run pytest tests/test_providers.py::test_model_override_wins_over_default  # single test
uv add <package>                               # add a dependency
uv add --dev <package>                         # add a dev-only dependency
```

## Adding a new topic

Create `examples/<topic>/` with `__init__.py`, a `main.py` exposing `run()`
(and a `if __name__ == "__main__": run()` block), and a `README.md`. Reuse
`core.providers.get_client()` / `get_model()` for provider access, then register
it in the `EXAMPLES` list in `main.py`.
