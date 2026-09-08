"""Offline tests for the phase 1 extractor — no network, stubbed model replies."""

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from project_phase_1.extractor import PersonExtractor, json_object

SAMPLE_TEXT = "Rahul Kumar, 32, works at Infosys as a senior developer."


class StubClient:
    """Stands in for the OpenAI client, replaying a canned reply."""

    def __init__(self, reply: str | None) -> None:
        message = SimpleNamespace(content=reply)
        response = SimpleNamespace(choices=[SimpleNamespace(message=message)])
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=lambda **_: response))


def extract(reply: str | None, text: str = SAMPLE_TEXT):
    return PersonExtractor(client=StubClient(reply), model="stub-model").extract(text)


def test_full_reply_maps_onto_every_field():
    person = extract(
        '{"name": "Rahul Kumar", "age": 32, "company": "Infosys", '
        '"role": "senior developer", "city": "Chennai", "email": "rahul@example.com"}'
    )
    assert person.name == "Rahul Kumar"
    assert person.age == 32
    assert person.email == "rahul@example.com"


def test_missing_fields_default_to_none():
    person = extract('{"name": "Rahul Kumar"}')
    assert (person.age, person.company, person.role, person.city, person.email) == (None,) * 5


def test_reply_wrapped_in_fences_and_prose_still_parses():
    person = extract('Sure! ```json\n{"name": "Rahul Kumar", "age": 32}\n```')
    assert person.age == 32


def test_empty_prompt_is_rejected_before_calling_the_model():
    with pytest.raises(ValueError, match="prompt is empty"):
        extract("{}", text="   ")


@pytest.mark.parametrize("reply", [None, "", "I could not find a person."])
def test_reply_without_json_raises(reply):
    with pytest.raises(ValueError, match="No JSON object"):
        extract(reply)


@pytest.mark.parametrize(
    "reply",
    [
        '{"age": 32}',                                    # name is required
        '{"name": "Rahul", "age": -1}',                   # age below floor
        '{"name": "Rahul", "age": 200}',                  # age above ceiling
        '{"name": "Rahul", "age": "thirty-two"}',         # unparseable age
        '{"name": "Rahul", "email": "not-an-email"}',     # fails the email pattern
    ],
)
def test_invalid_payloads_are_rejected(reply):
    with pytest.raises(ValidationError):
        extract(reply)


def test_json_object_keeps_the_outermost_braces():
    assert json_object('noise {"a": {"b": 1}} tail') == '{"a": {"b": 1}}'
