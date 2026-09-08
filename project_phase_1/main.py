"""Phase 1 entry point: prompt for text, print the extracted person as JSON."""

from project_phase_1.extractor import PersonExtractor

SAMPLE = (
    "Rahul Kumar, 32, works at Infosys as a senior developer. "
    "He lives in Chennai. Email is rahul@example.com"
)


def run() -> None:
    text = input("Text about a person (Enter to use the sample):\n> ").strip() or SAMPLE
    print(f"\nExtracting from:\n  {text}\n")

    person = PersonExtractor().extract(text)
    print(person.model_dump_json(indent=2))


if __name__ == "__main__":
    run()
