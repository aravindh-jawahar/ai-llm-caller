"""The extractor: free text in, validated PersonDetails out.

The LLM is asked for JSON matching PersonDetails' own schema, so the prompt and
the model never drift apart. Pydantic validates the reply, turning a bad answer
into a clear error instead of silently wrong data.
"""

import json

from core.providers import get_client, get_model
from project_phase_1.models import PersonDetails


def json_object(reply: str | None) -> str:
    """Slice the JSON object out of a reply that may carry prose or code fences."""
    text = reply or ""
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"No JSON object in the model's reply: {text!r}")
    return text[start : end + 1]


class PersonExtractor:
    """Extracts person details from text using an OpenAI-compatible chat model."""

    SYSTEM_PROMPT = (
        "You extract structured data about a person. Reply with ONLY valid JSON "
        "matching the given schema — no prose, no markdown fences. Use null for "
        "any field the text does not state; never invent a value."
    )

    def __init__(self, client=None, model: str | None = None) -> None:
        # Injectable so tests can run without a network call.
        self._client = client or get_client()
        self._model = model or get_model()

    def extract(self, text: str) -> PersonDetails:
        if not text.strip():
            raise ValueError("Nothing to extract: the prompt is empty.")
        return PersonDetails.model_validate_json(json_object(self._ask(text)))

    def _ask(self, text: str) -> str | None:
        schema = json.dumps(PersonDetails.model_json_schema(), indent=2)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": f"JSON schema:\n{schema}\n\nText:\n{text}"},
            ],
            temperature=0,  # extraction should be repeatable, not creative
        )
        return response.choices[0].message.content
