"""Topic 4 — Annotated types (reusable constraints).

WHEN IT MATTERS: When the SAME rule appears on many fields across many models
(a customer_id format, a non-empty trimmed string, a positive amount), copying a
@field_validator everywhere drifts out of sync. Annotated[type, Validator] bakes
the rule into a named type you import and reuse. AfterValidator runs on the typed
value; BeforeValidator runs on raw input (cleaning). This is how mature codebases
build a small library of domain types.
"""

from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, ValidationError


def _valid_customer_id(v: str) -> str:
    if not (v.startswith("CUST-") and len(v) == 10):
        raise ValueError("must start with 'CUST-' and be exactly 10 chars")
    return v


def _strip_title(v: str) -> str:
    return v.strip().title()


# Reusable domain types — import these into any model.
CustomerId = Annotated[str, AfterValidator(_valid_customer_id)]
CleanName = Annotated[str, BeforeValidator(_strip_title)]


class Customer(BaseModel):
    name: CleanName
    customer_id: CustomerId
    loyalty_points: int = 0


def run() -> None:
    print("=" * 64)
    print("TOPIC 4 — Annotated types")
    print("=" * 64)

    print("\n✅ Valid case (name cleaned by BeforeValidator, id checked by AfterValidator):")
    ok = Customer(name="  ada LOVELACE ", customer_id="CUST-12345")
    print(ok.model_dump_json(indent=2))  # name -> "Ada Lovelace"

    print("\n❌ Invalid case (customer_id too short for the reusable CustomerId type):")
    try:
        Customer(name="Bob", customer_id="CUST-1")
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")


# 📝 YOUR TURN:
#   Create a reusable `PositivePoints = Annotated[int, AfterValidator(...)]` that
#   rejects negative values, and apply it to `loyalty_points`. Then reuse the
#   SAME type on a second model to prove the point of Annotated.

if __name__ == "__main__":
    run()
