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

## Working agreements

### Development

- Clean code first: clear names, small functions, no dead code.
- Model each topic with classes and a thin abstraction over the provider —
  hide the vendor detail, expose the concept being taught. Keep the
  abstraction to one layer; no interface with a single implementation.
- Fewest lines that stay readable. Delete before adding.
- Respect the architecture: AI logic in `examples/<topic>/`, shared plumbing
  in `core/`. Nothing topic-specific leaks into `core/`.
- Install tooling through `uv` (`uv add --dev …`) so the lockfile stays the
  source of truth. Prefer established, well-maintained tools over bespoke
  scripts.
- Record findings and design decisions in the README — the topic's own
  `README.md` for topic-specific notes, the root one for cross-cutting ones.

### PR flow

- Never commit straight to `main`. Branch, do the task, open a PR.
- PR description says what changed, why, and how it was verified.
- Every task gets a ticket number (`AI-001`, `AI-002`, …) logged in the
  "Task log" table in the root `README.md`. Reference it in the branch name,
  commit subject, and PR title — never in source comments.

### Task completion checklist

A task is done only when every box is ticked — pushing is not the finish line,
the open PR is.

1. Ticket number assigned and added to the Task log in the root `README.md`.
2. Code written on a branch named after the ticket (`AI-003-short-description`).
3. `uv run pytest` passes, and the example itself was run if one changed.
4. Edge cases covered by a test, not just the happy path.
5. Decisions and findings written into the relevant `README.md`.
6. Branch pushed **and** a pull request opened — never stop at the push.
7. PR title carries the ticket; the body says what, why, and how it was verified.
8. Task log row updated to reflect the real status.

### QA

- Run it before pushing: `uv run pytest`, plus the example itself
  (`uv run python -m examples.<topic>.main`) when the change touches one.
- Cover edge cases, not just the happy path: empty and missing input,
  malformed model output, absent API key, network failure.
- Report actual results. If something is untested or broken, say so in the PR.
