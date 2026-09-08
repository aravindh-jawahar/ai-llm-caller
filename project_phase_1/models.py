"""The target shape for extraction: what we want to know about a person."""

from pydantic import BaseModel, Field

# Deliberately loose — enough to reject "not-an-email" without an extra dependency.
EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class PersonDetails(BaseModel):
    """Person details pulled out of free text. Everything but the name is optional
    because real prompts rarely mention every field."""

    name: str = Field(description="The person's full name")
    age: int | None = Field(default=None, ge=0, le=120, description="Age in years, null if not stated")
    company: str | None = Field(default=None, description="Employer or organisation")
    role: str | None = Field(default=None, description="Job title or role")
    city: str | None = Field(default=None, description="City they live in")
    email: str | None = Field(default=None, pattern=EMAIL_PATTERN, description="Email address")
