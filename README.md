Easiest way to test with your own prompt is the chat_loop example — it lets you type anything at a prompt. Here are your options:

Option 1 — Interactive chat (type your own prompt)

uv run python -m examples.chat_loop.main
You'll see a you> prompt. Type any question, press Enter, and the model replies. Type exit (or quit) to stop.

Option 2 — The menu

uv run main.py
Pick a number (1 = basic, 2 = streaming, 3 = chat).

Option 3 — Quick one-shot examples

uv run python -m examples.llm_basics.main # fixed "explain an LLM" prompt
uv run python -m examples.streaming.main # fixed "poem" prompt, streamed

## Task log

| Ticket | Task | Status | Notes |
| ------ | ---- | ------ | ----- |
| AI-001 | Initial playground: core provider client + example topics | Done | |
| AI-002 | Document development, PR, and QA working agreements | Done | Agreements in `CLAUDE.md`; this task log added |
| AI-003 | AI structured data extractor (`project_phase_1/`) | Done | Person details from free text; logic to be tuned further |
| AI-004 | CI: run the test suite on every PR and on merges to `main` | In review | `.github/workflows/tests.yml`; make it a required check once merged |
