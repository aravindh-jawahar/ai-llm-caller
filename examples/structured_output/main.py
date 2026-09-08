"""Structured output: turn free text into a validated Pydantic object.

LLMs return text. Often we want *data* — with known fields and types. The
pattern here: define a Pydantic model, ask the model to fill it in as JSON, then
validate the reply against the model. If the JSON is malformed or a field is the
wrong type, Pydantic raises a clear error instead of letting bad data through.
"""

import json

from pydantic import BaseModel, Field

from core.providers import get_client, get_model


class Person(BaseModel):
    """The shape of data we want back from the model."""

    name: str = Field(description="The person's full name")
    age: int | None = Field(description="Age in years, or null if unknown")
    occupation: str = Field(description="Their main job or role")
    skills: list[str] = Field(description="Notable skills or areas of expertise")


BIO = (
    "Ada Lovelace was a 19th-century English mathematician, widely regarded as "
    "the first computer programmer. She collaborated with Charles Babbage on the "
    "Analytical Engine and was skilled in mathematics, logic, and writing "
    "algorithms."
)


def _extract_json(text: str) -> str:
    """Pull the JSON object out of the reply, tolerating markdown code fences."""
    text = text.strip()
    if text.startswith("```"):
        # drop the opening fence (``` or ```json) and anything after a closing fence
        text = text.split("```")[1]
        if text.lstrip().startswith("json"):
            text = text.lstrip()[4:]
    start, end = text.find("{"), text.rfind("}")
    return text[start : end + 1] if start != -1 and end != -1 else text


def run() -> None:
    client = get_client()
    model = get_model()

    # model_json_schema() gives the model an exact description of the fields.
    schema = json.dumps(Person.model_json_schema(), indent=2)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured data. Reply with ONLY valid JSON "
                    "matching the given schema — no prose, no markdown fences."
                ),
            },
            {
                "role": "user",
                "content": f"JSON schema:\n{schema}\n\nExtract a person from this text:\n{BIO}",
            },
        ],
        temperature=0,  # deterministic — we want reliable extraction, not creativity
    )

    raw_reply = response.choices[0].message.content
    print("Raw model reply:\n", raw_reply, "\n")

    # The key step: parse + validate in one call. Raises if the data is bad.
    person = Person.model_validate_json(_extract_json(raw_reply))

    print("Validated Person object:")
    print("  name:      ", person.name)
    print("  age:       ", person.age)
    print("  occupation:", person.occupation)
    print("  skills:    ", ", ".join(person.skills))
    print("\nType is:", type(person).__name__, "— fully typed, safe to use in code.")


if __name__ == "__main__":
    run()
