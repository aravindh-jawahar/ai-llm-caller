"""Topic 5 — field_serializer and computed_field.

WHEN IT MATTERS: The shape you VALIDATE isn't always the shape you EMIT.
@field_serializer customizes how a field is rendered in model_dump()/JSON
(e.g. join a skills list into a string, mask a secret, format a date) without
changing the stored value. @computed_field exposes a derived, read-only value
(a tier from points, a display name) that appears in output and JSON schema but
isn't an input field. Both are core to clean API responses.
"""

from pydantic import BaseModel, computed_field, field_serializer


class Customer(BaseModel):
    name: str
    customer_id: str
    skills: list[str]
    loyalty_points: int = 0

    @computed_field  # type: ignore[prop-decorator]
    @property
    def tier(self) -> str:
        # Derived from points — not an input, always consistent.
        if self.loyalty_points >= 10_000:
            return "platinum"
        if self.loyalty_points >= 5_000:
            return "gold"
        if self.loyalty_points >= 1_000:
            return "silver"
        return "bronze"

    @field_serializer("skills")
    def serialize_skills(self, skills: list[str]) -> str:
        # Stored as a list, emitted as a comma-separated string.
        return ", ".join(skills)


def run() -> None:
    print("=" * 64)
    print("TOPIC 5 — field_serializer & computed_field")
    print("=" * 64)

    c = Customer(
        name="Ada Lovelace",
        customer_id="CUST-12345",
        skills=["Mathematics", "Logic", "Algorithm Design"],
        loyalty_points=7_500,
    )

    print("\nIn-memory value (skills is still a real list):")
    print("  c.skills =", c.skills)
    print("  c.tier   =", c.tier, "(computed, read-only)")

    print("\nSerialized output (skills joined; tier included):")
    print(c.model_dump_json(indent=2))


# 📝 YOUR TURN:
#   Add a computed_field `display_name` that returns "<name> (<customer_id>)",
#   e.g. "Ada Lovelace (CUST-12345)". Confirm it shows up in model_dump_json()
#   but can't be passed in as a constructor argument.

if __name__ == "__main__":
    run()
