"""httpx basics: call a real REST API and read the JSON response.

Fetches MoneySmart's credit-card product listing and prints a short summary.
Demonstrates the httpx essentials: a Client, query params, a timeout,
raise_for_status(), and parsing JSON.
"""

import httpx

from examples.httpx_basics.models.product import Product

API_URL = "https://api.moneysmart.sg/product-listing/v2/product_listings"


def create_product_from_json(data: dict) -> "Product":
    """Create a Product instance from a JSON object."""
    return Product(
        id=data.get("id", ""),
        type=data.get("type", ""),
        slug=data.get("attributes", {}).get("slug", ""),
        partner=data.get("attributes", {}).get("partner", False),
        pdp_url=data.get("attributes", {}).get("pdp_url", ""),
        plp_url=data.get("attributes", {}).get("plp_url", ""),
    )

def run() -> None:
    # A Client is the recommended entry point: it pools connections and lets you
    # set shared config (timeout, headers, base_url). Use it as a context manager
    # so the connection is cleaned up. Always set a timeout in real code.
    with httpx.Client(timeout=30.0) as client:
        # `params` builds the query string safely (?path=credit-cards).
        response = client.get(API_URL, params={"path": "credit-cards"})

    # Raises httpx.HTTPStatusError for 4xx/5xx so failures are loud, not silent.
    response.raise_for_status()

    print(f"GET {response.url}")
    print(f"Status: {response.status_code} {response.reason_phrase}")
    print(f"Elapsed: {response.elapsed.total_seconds():.2f}s")
    print(f"Content-Type: {response.headers.get('content-type')}\n")

    # .json() parses the response body into Python dicts/lists.
    data = response.json()
    products = data.get("products", [])
    print(f"Found {len(products)} credit-card products. First 10:\n")

    for product in products[:30]:
        attrs = product.get("attributes", {})
        name = attrs.get("name", "<no name>")
        # `provider` is a nested JSON:API-style object.
        provider = attrs.get("provider", {}).get("attributes", {}).get("name", "?")
        category = attrs.get("category_name", "?")
        print(f"  - {name}  ({provider} · {category})")
        product = create_product_from_json(product)  # Create a Product instance from the JSON data

        print(f"    product: {product.model_dump_json(indent=2)}\n")


if __name__ == "__main__":
    run()
