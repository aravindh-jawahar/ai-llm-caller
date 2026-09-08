"""Topic 9 — ValidationError handling patterns.

WHEN IT MATTERS: In production you rarely let a ValidationError crash the
process. You catch it and turn it into a structured HTTP 422 response, a log
line, or a row sent to a dead-letter queue. `e.errors()` gives a list of dicts
(loc, type, msg, input) you can map to field-level API errors. `e.json()` gives
that same structure as a JSON string. `e.error_count()` is handy for metrics.
Never `str(e)` into an API response — parse the structure instead.
"""

from pydantic import BaseModel, Field, ValidationError


class Customer(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0)
    customer_id: str = Field(pattern=r"^CUST-\d{5}$")


def safe_parse(data: dict) -> Customer | None:
    """Real-world pattern: validate, but degrade gracefully on failure."""
    try:
        return Customer.model_validate(data)
    except ValidationError as e:
        print(f"  [reject] {e.error_count()} problem(s):")
        for err in e.errors():
            loc = ".".join(map(str, err["loc"]))
            print(f"    - field={loc!r} type={err['type']!r} msg={err['msg']!r} got={err['input']!r}")
        return None


def run() -> None:
    print("=" * 64)
    print("TOPIC 9 — ValidationError handling")
    print("=" * 64)

    print("\n✅ Good data returns a model:")
    print("  ->", safe_parse({"name": "Ada", "age": 36, "customer_id": "CUST-12345"}))

    print("\n❌ Bad data returns None, with structured errors logged:")
    result = safe_parse({"name": "", "age": -1, "customer_id": "nope"})
    print("  ->", result)

    print("\n📦 The same errors as a JSON string (ready for an HTTP 422 body):")
    try:
        Customer.model_validate({"name": "", "age": -1, "customer_id": "nope"})
    except ValidationError as e:
        print(e.json(indent=2))


# 📝 YOUR TURN:
#   Extend safe_parse to return a tuple (customer | None, errors: list[dict]) so
#   the caller can both branch on success AND forward the structured errors to an
#   API response. Keep using e.errors(), not str(e).

if __name__ == "__main__":
    run()
