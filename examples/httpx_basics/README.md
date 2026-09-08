# 06 · httpx basics

Make a real HTTP request to a REST API and read the JSON response, using
[httpx](https://www.python-httpx.org/) — a modern requests-style HTTP client
(and the same library the OpenAI SDK uses under the hood).

## Run

```bash
uv run python -m examples.httpx_basics.main
```

Calls the MoneySmart product-listing API:
`https://api.moneysmart.sg/product-listing/v2/product_listings?path=credit-cards`
and prints the first 10 credit cards with their provider and category.

## What to notice

- **`httpx.Client()`** as a context manager — pools connections and cleans up.
  Prefer it over the module-level `httpx.get()` shortcut in real code.
- **`params={...}`** builds the query string safely (URL-encoding for you).
- **`timeout=30.0`** — httpx has sane timeouts by default; always set one
  explicitly for external calls so a hung server can't hang your app.
- **`response.raise_for_status()`** turns a 4xx/5xx into an exception instead of
  letting a bad response flow on as if it succeeded.
- **`response.json()`** parses the body into Python objects. Other useful bits:
  `response.status_code`, `response.headers`, `response.elapsed`, `response.url`.

## Next ideas

- Wrap the parsed products in a Pydantic model (see
  `examples/data_model_and_validations`) to validate the API shape.
- Try the async version: `httpx.AsyncClient` with `await client.get(...)`.
