"""AI Demo App — entry point.

Lists the available examples and runs the one you pick. Each example can also be
run directly, e.g.:

    uv run python -m examples.llm_basics.main
"""

import importlib
# (importable package, one-line description)
EXAMPLES: list[tuple[str, str]] = [
    ("examples.llm_basics", "Basic non-streaming LLM call"),
    ("examples.streaming", "Stream tokens as they arrive"),
    ("examples.chat_loop", "Multi-turn chat that remembers context"),
    ("examples.structured_output", "Extract validated typed data with Pydantic"),
    ("examples.httpx_basics", "Call a real REST API with httpx"),
    ("project_phase_1", "Extract person details from any prompt into a typed model"),
]


def main() -> None:
    print("AI Demo App — pick an example:\n")
    for i, (package, desc) in enumerate(EXAMPLES, start=1):
        print(f"  {i}. {package.rpartition('.')[2]} — {desc}")
    print()

    choice = input("Enter a number (or 'q' to quit): ").strip()
    if choice.lower() in {"q", "quit", "exit"}:
        return

    try:
        package = EXAMPLES[int(choice) - 1][0]
    except (ValueError, IndexError):
        print(f"'{choice}' is not a valid choice.")
        return

    module = importlib.import_module(f"{package}.main")
    print()
    module.run()


if __name__ == "__main__":
    main()
