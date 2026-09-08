from pydantic import BaseModel, Field

class Person(BaseModel):
    """The shape of data we want back from the model."""

    name: str = Field(description="The person's full name")
    age: int | None = Field(description="Age in years, or null if unknown")
    occupation: str = Field(description="Their main job or role")
    skills: list[str] = Field(description="Notable skills or areas of expertise")


class Customer(Person):
    """A customer is a person with a customer ID and loyalty points."""

    customer_id: str = Field(description="Unique identifier for the customer")
    loyalty_points: int = Field(description="Loyalty points accumulated by the customer")