"""Topic 1 — Field-level validations (constraints via Field()).

WHEN IT MATTERS: Constraints are your first line of defense at the system
boundary — API request bodies, LLM structured output, CSV rows. They reject
garbage (empty names, negative balances, malformed IDs) declaratively, before
the bad value ever reaches your business logic or database. Your current
Customer model accepts a negative loyalty_points and an empty name; that's a
production incident waiting to happen.
"""

from pydantic import BaseModel, Field, ValidationError


class Customer(BaseModel):
    # str: length bounds. num: ge/le (>=/<=), gt/lt (>/<). str: regex `pattern`.
    name: str = Field(min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=150)
    occupation: str = Field(min_length=1, max_length=100)
    skills: list[str] = Field(min_length=1, max_length=20)  # 1..20 items
    customer_id: str = Field(pattern=r"^CUST-\d{5}$")       # e.g. CUST-12345
    loyalty_points: int = Field(default=0, ge=0)


def run() -> None:
    print("=" * 64)
    print("TOPIC 1 — Field-level validations")
    print("=" * 64)

    print("\n✅ Valid case:")
    ok = Customer(
        name="Ada Lovelace",
        age=36,
        occupation="Mathematician",
        skills=["Mathematics", "Logic"],
        customer_id="CUST-00001",
        loyalty_points=1500,
    )
    print(ok.model_dump_json(indent=2))

    print("\n❌ Invalid case (empty name, negative points, bad id, no skills):")
    try:
        Customer(
            name="",
            age=200,
            occupation="Mathematician",
            skills=[],
            customer_id="12345",
            loyalty_points=-50,
        )
    except ValidationError as e:
        print(f"{e.error_count()} errors:")
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")


# 📝 YOUR TURN:
#   Add constraints so `occupation` is at most 50 characters, and `age` must be
#   at least 18 (an adult customer). Then prove it: construct a Customer with
#   age=17 and confirm you get a ValidationError on `age`.

if __name__ == "__main__":
    run()
