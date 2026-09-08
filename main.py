"""AI Demo App — entry point.

Lists the available examples and runs the one you pick. Each example can also be
run directly, e.g.:

    uv run python -m examples.llm_basics.main
"""

import importlib

# (module name under examples/, one-line description)
EXAMPLES: list[tuple[str, str]] = [
    ("llm_basics", "Basic non-streaming LLM call"),
    ("streaming", "Stream tokens as they arrive"),
    ("chat_loop", "Multi-turn chat that remembers context"),
    ("structured_output", "Extract validated typed data with Pydantic"),
    ("httpx_basics", "Call a real REST API with httpx"),
]


def main() -> None:
    print("AI Demo App — pick an example:\n")
    for i, (name, desc) in enumerate(EXAMPLES, start=1):
        print(f"  {i}. {name} — {desc}")
    print()

    choice = input("Enter a number (or 'q' to quit): ").strip()
    if choice.lower() in {"q", "quit", "exit"}:
        return

    try:
        name = EXAMPLES[int(choice) - 1][0]
    except (ValueError, IndexError):
        print(f"'{choice}' is not a valid choice.")
        return

    module = importlib.import_module(f"examples.{name}.main")
    print()
    module.run()


if __name__ == "__main__":
    main()
