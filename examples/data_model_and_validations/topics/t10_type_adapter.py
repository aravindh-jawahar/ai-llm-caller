"""Topic 10 — TypeAdapter (validating non-BaseModel types).

WHEN IT MATTERS: Not everything you validate is a BaseModel. An API returns a
LIST of customers, a config is a dict[str, int], an LLM returns a bare
list[str]. Wrapping these in a throwaway model is clumsy. TypeAdapter gives you
full Pydantic validation, coercion, JSON parsing, and schema generation for ANY
type annotation — list[Customer], dict[str, Customer], tuple[int, str] — without
a model class. Build the adapter once, reuse it.
"""

from pydantic import BaseModel, Field, TypeAdapter, ValidationError


class Customer(BaseModel):
    name: str
    customer_id: str = Field(pattern=r"^CUST-\d{5}$")
    loyalty_points: int = 0


def run() -> None:
    print("=" * 64)
    print("TOPIC 10 — TypeAdapter")
    print("=" * 64)

    # Validate a LIST of customers coming from an API — no wrapper model needed.
    customers_adapter = TypeAdapter(list[Customer])

    print("\n✅ Validate + parse a JSON array straight into list[Customer]:")
    raw_json = (
        '[{"name": "Ada", "customer_id": "CUST-00001", "loyalty_points": 900},'
        ' {"name": "Grace", "customer_id": "CUST-00002"}]'
    )
    customers = customers_adapter.validate_json(raw_json)
    print(f"  parsed {len(customers)} customers; first = {customers[0].name}")

    print("\n✅ TypeAdapter also validates bare containers (with coercion):")
    scores = TypeAdapter(dict[str, int])
    print("  ->", scores.validate_python({"ada": "10", "grace": 20}))  # "10" coerced

    print("\n❌ One bad element fails the whole list, with an index in the loc:")
    try:
        customers_adapter.validate_python([{"name": "Bad", "customer_id": "oops"}])
    except ValidationError as e:
        for err in e.errors():
            print(f"  - {'.'.join(map(str, err['loc']))}: {err['msg']}")


# 📝 YOUR TURN:
#   Build a TypeAdapter for dict[str, Customer] (a lookup keyed by customer_id)
#   and validate {"CUST-00001": {...}, "CUST-00002": {...}}. Then call
#   .json_schema() on it and notice you get a schema for a type with no class.

if __name__ == "__main__":
    run()
