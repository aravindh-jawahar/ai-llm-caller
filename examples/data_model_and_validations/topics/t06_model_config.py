"""Topic 6 — model_config (ConfigDict).

WHEN IT MATTERS: model_config sets model-wide policy. `extra="forbid"` rejects
unexpected keys — critical for API bodies and LLM output, where a silently
ignored typo'd field ("loyalty_point") means data loss. `str_strip_whitespace`
trims every str field. `validate_assignment` re-validates on attribute set (so
`c.age = -5` raises instead of corrupting state). `frozen=True` makes instances
immutable + hashable. Defaults are permissive; production configs are strict.
"""

from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Customer(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )

    name: str
    age: int = Field(ge=0)
    loyalty_points: int = 0


def run() -> None:
    print("=" * 64)
    print("TOPIC 6 — model_config (ConfigDict)")
    print("=" * 64)

    print("\n✅ str_strip_whitespace trims input:")
    c = Customer(name="  Ada Lovelace  ", age=36)
    print(f"  name = {c.name!r}")

    print("\n❌ extra='forbid' rejects an unknown/typo'd field ('loyalty_point'):")
    try:
        Customer(name="Ada", age=36, loyalty_point=100)  # note: missing 's'
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")

    print("\n❌ validate_assignment catches bad mutation AFTER construction:")
    try:
        c.age = -5
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")


# 📝 YOUR TURN:
#   Make a `frozen=True` variant of Customer. Confirm that (a) `c.name = "x"`
#   raises after construction, and (b) a frozen instance is now hashable
#   (try putting two of them in a set).

if __name__ == "__main__":
    run()
