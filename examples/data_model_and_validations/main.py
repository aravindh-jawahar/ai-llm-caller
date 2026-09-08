"""Ask an AI architect how a full-stack dev can become AI-driven.

Note the two message roles:
- `system` sets *who the assistant is* (its persona / behavior).
- `user` carries the *actual request*. A request with only a system message
  and no user message returns nothing (or errors) on most models.
"""

from core.providers import get_client, get_model
from examples.data_model_and_validations.models.person import Person
from examples.data_model_and_validations.models.person import Customer

def create_person(person) -> Person:
    """Convert a dict to a Person object, validating the data."""
    return Person(**person)
    
def create_customer(customer) -> Customer:
    """Convert a dict to a Customer object, validating the data."""
    return Customer(**customer)

def run() -> None:
    client = get_client()
    model = get_model()

    # response = client.chat.completions.create(
    #     model=model,
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are an AI technical architect who gives clear, practical guidance.",
    #         },
    #         {
    #             "role": "user",
    #             "content": (
    #                 "How can a full-stack developer grow into an AI-driven "
    #                 "full-stack developer? Give a concise, actionable roadmap."
    #             ),
    #         },
    #     ],
    #     temperature=0.7,
    # )
    # print(response.model_dump_json())
    print(create_person({
        "name": "Ada Lovelace",
        "age": 36,
        "occupation": "Mathematician",
        "skills": ["Mathematics", "Logic", "Algorithm Design"],
    }).model_dump_json(indent=2))

    print(create_customer({
        "name": "Alan Turing",
        "age": 41,
        "occupation": "Computer Scientist",
        "skills": ["Cryptography", "Mathematics", "Artificial Intelligence"],
        "customer_id": "CUST12345",
        "loyalty_points": 1500,
    }).model_dump_json(indent=2))

if __name__ == "__main__":
    run()
