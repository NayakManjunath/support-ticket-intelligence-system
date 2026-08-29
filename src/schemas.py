from pydantic import BaseModel, Field

from src.taxonomy import Category, Priority, Sentiment


class TicketAnalysis(BaseModel):
    category: Category = Field(
        description=(
            "The primary category of the customer support issue. "
            "Must be one of the predefined categories."
        )
    )

    priority: Priority = Field(
        description=(
            "The urgency of the support ticket based on "
            "business impact, urgency, financial impact, "
            "account access, and security concerns."
        )
    )

    sentiment: Sentiment = Field(
        description=(
            "The customer's emotional sentiment expressed "
            "in the support ticket."
        )
    )

    issue: str = Field(
        min_length=5,
        description=(
            "A concise description of the customer's actual "
            "support issue."
        )
    )

    summary: str = Field(
        min_length=10,
        description=(
            "A concise business-friendly summary of the "
            "customer's problem."
        )
    )

    recommended_action: str = Field(
        min_length=10,
        description=(
            "A practical action that the support team should "
            "take to resolve or investigate the issue."
        )
    )
