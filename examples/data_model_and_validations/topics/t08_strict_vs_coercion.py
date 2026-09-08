"""Topic 8 — strict mode vs. default coercion.

WHEN IT MATTERS: By default Pydantic is lax and coerces: the string "42"
becomes int 42, "true" becomes True. Convenient for HTTP query params and
loose sources — dangerous when types carry meaning and silent coercion hides
a bug (a JSON payload sending "1500" as a string when your DB column is a real
int). Strict mode refuses to coerce and demands the exact type. You can go
strict per-field (Field(strict=True)), per-model (ConfigDict(strict=True)), or
per-call (model_validate(data, strict=True)).
"""

from pydantic import BaseModel, Field, ValidationError


class Customer(BaseModel):
    name: str
    age: int                              # lax by default → coerces "36" to 36
    loyalty_points: int = Field(strict=True)   # this field refuses coercion


def run() -> None:
    print("=" * 64)
    print("TOPIC 8 — strict vs. coercion")
    print("=" * 64)

    print("\n✅ Default coercion: age='36' (string) becomes int 36:")
    c = Customer(name="Ada", age="36", loyalty_points=1500)
    print(f"  c.age = {c.age!r}  (type: {type(c.age).__name__})")

    print("\n❌ Per-field strict: loyalty_points='1500' (string) is rejected:")
    try:
        Customer(name="Ada", age=36, loyalty_points="1500")
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")

    print("\n❌ Per-call strict=True: now even age='36' is rejected:")
    try:
        Customer.model_validate({"name": "Ada", "age": "36", "loyalty_points": 1500}, strict=True)
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")


# 📝 YOUR TURN:
#   Remove strict=True from loyalty_points and instead set
#   model_config = ConfigDict(strict=True) on the whole model. Predict which of
#   the three cases above still pass, then run it to check yourself.

if __name__ == "__main__":
    run()
