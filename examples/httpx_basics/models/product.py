from pydantic import BaseModel, Field, model_validator


class Product(BaseModel):
    id: str
    type: str
    slug: str
    partner: bool
    # Product Detail Page: the category path PLUS a slug (…/credit-cards/<slug>).
    pdp_url: str = Field(pattern=r"^https://www\.moneysmart\.sg/credit-cards/.+$")
    # Product Listing Page: the category page itself, no slug (…/credit-cards).
    plp_url: str = Field(pattern=r"^https://www\.moneysmart\.sg/credit-cards$")
    comment: str | None = Field(default=None, description="Optional comment about the product")

    @classmethod
    def from_json(cls, data: dict) -> "Product":
        """Create a Product instance from a JSON object."""
        return cls(
            id=data.get("id", ""),
            type=data.get("type", ""),
            slug=data.get("attributes", {}).get("slug", ""),
            partner=data.get("attributes", {}).get("partner", False),
            pdp_url=data.get("attributes", {}).get("pdp_url", ""),
            plp_url=data.get("attributes", {}).get("plp_url", ""),
        )
    
    @model_validator(mode="after")
    def generate_comment(self) -> "Product":
        """Generate a comment based on the product's partner status."""
        if self.partner:
            self.comment = "This is a partner product."
        else:
            self.comment = "This is not a partner product."
        return self
