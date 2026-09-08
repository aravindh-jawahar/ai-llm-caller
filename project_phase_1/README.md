# Project Phase 1 — AI Structured Data Extractor

Free text in, a validated `PersonDetails` object out.

```bash
uv run python -m project_phase_1.main   # Enter for the sample, or paste your own text
uv run pytest tests/test_person_extractor.py
```

## Process

1. Read a prompt (any text mentioning a person).
2. Send it to the model together with `PersonDetails.model_json_schema()`.
3. Slice the JSON object out of the reply and validate it with Pydantic.
4. Return the typed object.

## Layout

| File | Responsibility |
| ---- | -------------- |
| `models.py` | `PersonDetails` — the target shape and its validation rules |
| `extractor.py` | `PersonExtractor` — the LLM call and reply parsing |
| `main.py` | `run()` — read input, print the result |

## Decisions

- **The schema comes from the model class**, not a hand-written prompt. Adding a
  field to `PersonDetails` changes what the LLM is asked for — the two cannot drift.
- **`PersonExtractor` takes an optional client**, so tests replay canned replies
  and the suite stays offline.
- **Only `name` is required.** Real prompts skip fields; forcing them invites the
  LLM to invent values, so the system prompt says use null and the model allows it.
- **Email is a regex `Field`, not `EmailStr`** — that would pull in
  `email-validator` for one field. Swap it in if real deliverability matters.
- **`temperature=0`** — extraction should be repeatable.
- **Reply parsing takes the outermost `{`…`}`.** This handles prose preambles and
  ```` ```json ```` fences in one line, so no fence-stripping logic is needed.

## Findings

- `openai/gpt-oss-20b` on NVIDIA returned clean JSON for the sample with no fences.
- Given a sparse prompt ("Priya is a designer.") it correctly returned nulls
  rather than guessing an age or city.
- Verified: `20 passed` on `uv run pytest`; both live runs above produced valid objects.

## Next (phase 1 tuning)

Retry on a validation failure, batch extraction, and provider-native JSON mode
where available.
