"""Topic 3 — Custom validators (@field_validator, @model_validator).

WHEN IT MATTERS: Field() constraints can't express logic. Use @field_validator
when one field needs custom rules or normalization (dedupe skills, canonicalize
an ID). Use @model_validator when a rule spans MULTIPLE fields (a 'platinum'
tier must have enough points). Mode matters: `before` sees the raw input (good
for cleaning/coercing); `after` sees the already-validated, typed value (good
for asserting invariants). Getting the mode wrong is a classic bug — a 'before'
validator that assumes an int will crash on the raw string.
"""

from pydantic import BaseModel, ValidationError, field_validator, model_validator


class Customer(BaseModel):
    name: str
    skills: list[str]
    customer_id: str
    loyalty_points: int = 0
    tier: str = "bronze"

    @field_validator("skills", mode="before")
    @classmethod
    def clean_skills(cls, v: list[str]) -> list[str]:
        # Runs on RAW input: strip whitespace, drop blanks, dedupe (case-insensitive).
        seen, out = set(), []
        for s in v:
            s = s.strip()
            if s and s.lower() not in seen:
                seen.add(s.lower())
                out.append(s)
        return out

    @field_validator("customer_id")  # default mode="after"
    @classmethod
    def check_id(cls, v: str) -> str:
        if not v.startswith("CUST-"):
            raise ValueError("customer_id must start with 'CUST-'")
        return v

    @model_validator(mode="after")
    def platinum_requires_points(self) -> "Customer":
        if self.tier == "platinum" and self.loyalty_points < 10_000:
            raise ValueError("platinum tier requires at least 10,000 loyalty_points")
        return self


def run() -> None:
    print("=" * 64)
    print("TOPIC 3 — Custom validators")
    print("=" * 64)

    print("\n✅ Valid case (skills cleaned + deduped, cross-field rule satisfied):")
    ok = Customer(
        name="Ada",
        skills=[" Math ", "math", "", "Logic"],
        customer_id="CUST-1",
        tier="platinum",
        loyalty_points=12_000,
    )
    print("cleaned skills:", ok.skills)
    print(ok.model_dump_json(indent=2))

    print("\n❌ Invalid case (platinum but only 500 points → model_validator fires):")
    try:
        Customer(name="Bob", skills=["x"], customer_id="CUST-2", tier="platinum", loyalty_points=500)
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc'])) or '<model>'}: {err['msg']}")


# 📝 YOUR TURN:
#   Write a @field_validator on `customer_id` that rejects it unless it starts
#   with "CUST-" AND is exactly 10 characters long (e.g. "CUST-12345" passes,
#   "CUST-1" fails). Decide: is this better as `before` or `after`? Why?

if __name__ == "__main__":
    run()
