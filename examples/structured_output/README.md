# 04 · Structured output (with Pydantic)

LLMs return text, but applications usually want **data** — fields with known
names and types. This example gets the model to extract a person's details from
a paragraph and return them as JSON, then validates that JSON into a typed
`Person` object using [Pydantic](https://docs.pydantic.dev/).

## Run

```bash
uv run python -m examples.structured_output.main
```

## What to notice

- **`class Person(BaseModel)`** defines the exact shape we want. Each `Field`
  has a description that we hand to the model.
- **`Person.model_json_schema()`** turns that class into a JSON schema string —
  a precise spec the model can follow.
- **`temperature=0`** makes extraction deterministic; we want reliability, not
  creativity.
- **`Person.model_validate_json(...)`** is the payoff: it parses the reply *and*
  checks every field's type in one step. If the model returns `"age": "old"`
  instead of a number, or omits a required field, Pydantic raises a clear
  `ValidationError` instead of letting bad data flow downstream.
- `_extract_json` is a small safety net: models sometimes wrap JSON in markdown
  ```` ```json ```` fences despite instructions, so we strip those before parsing.

## Why this matters

This is the foundation for reliable AI features: instead of fragile string
parsing, you get validated Python objects you can pass around with confidence.
It's the same idea behind "function calling" / "tool use," which we can explore
as a later topic.
