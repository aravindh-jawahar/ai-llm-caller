"""Topic 7 — alias / populate_by_name (external field-name mapping).

WHEN IT MATTERS: External JSON rarely matches your Python style. APIs send
camelCase ("customerId"), legacy systems send snake_case or odd keys. `alias`
maps the external name to your clean Python field. `populate_by_name=True` lets
you ALSO build the model with the Python name (essential for tests and internal
construction). `AliasChoices` accepts several possible incoming names. Emit the
external shape with model_dump(by_alias=True).
"""

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class Customer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    # Accept either "customerId" or "cust_id" on the way in.
    customer_id: str = Field(validation_alias=AliasChoices("customerId", "cust_id"),
                             serialization_alias="customerId")
    loyalty_points: int = Field(default=0, alias="loyaltyPoints")


def run() -> None:
    print("=" * 64)
    print("TOPIC 7 — alias / populate_by_name")
    print("=" * 64)

    print("\n✅ Build from an external camelCase API payload:")
    api_payload = {"name": "Ada", "customerId": "CUST-12345", "loyaltyPoints": 900}
    c = Customer.model_validate(api_payload)
    print(f"  c.customer_id = {c.customer_id!r}  (clean Python name internally)")

    print("\n✅ populate_by_name lets you also use Python field names (great in tests):")
    c2 = Customer(name="Bob", customer_id="CUST-54321", loyalty_points=10)
    print(f"  c2.customer_id = {c2.customer_id!r}")

    print("\n✅ AliasChoices also accepts the legacy 'cust_id' key:")
    c3 = Customer.model_validate({"name": "Grace", "cust_id": "CUST-99999"})
    print(f"  c3.customer_id = {c3.customer_id!r}")

    print("\nEmit back in external shape with by_alias=True:")
    print(c.model_dump_json(by_alias=True, indent=2))


# 📝 YOUR TURN:
#   Add a `full_name` field that accepts BOTH "fullName" and "name" from
#   incoming payloads via AliasChoices, but serializes as "fullName".
#   Validate a payload using each incoming key to prove both work.

if __name__ == "__main__":
    run()
