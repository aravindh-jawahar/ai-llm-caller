"""Topic 2 — Enums for fixed-choice fields.

WHEN IT MATTERS: Any field with a closed set of valid values — status,
tier, region, role — should be an Enum, not a free str. It rejects typos
("gold " / "diamond") at the boundary, gives you autocomplete + exhaustiveness
in code, and documents the allowed values in the JSON schema you hand to an LLM
or an API consumer. `str, Enum` serializes as the string; `IntEnum` as the int.
"""

from enum import Enum, IntEnum

from pydantic import BaseModel, Field, ValidationError


class LoyaltyTier(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class SupportLevel(IntEnum):
    BASIC = 1
    PRIORITY = 2
    DEDICATED = 3


class Customer(BaseModel):
    name: str
    tier: LoyaltyTier
    support_level: SupportLevel = SupportLevel.BASIC


def run() -> None:
    print("=" * 64)
    print("TOPIC 2 — Enums")
    print("=" * 64)

    print("\n✅ Valid case (string coerced into the enum member):")
    ok = Customer(name="Ada Lovelace", tier="gold", support_level=2)
    print(ok.model_dump_json(indent=2))
    print("type of tier:", type(ok.tier).__name__, "| is GOLD?", ok.tier is LoyaltyTier.GOLD)

    print("\n❌ Invalid case (tier='diamond' is not a member):")
    try:
        Customer(name="Ada", tier="diamond")
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")


# 📝 YOUR TURN:
#   Add a required `region` field backed by a str Enum with members
#   APAC, EMEA, AMER. Construct one Customer with region="APAC" (works) and one
#   with region="MOON" (should fail). Bonus: what does model_json_schema() now
#   show for `region`?

if __name__ == "__main__":
    run()
