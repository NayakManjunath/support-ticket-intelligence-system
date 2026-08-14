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

# from pydantic import BaseModel, Field

# from src.taxonomy import Category, Priority, Sentiment

# class TicketAnalysis(BaseModel):
#     category: Category = Field(

#         description = (
#             "The primary category of the customer support issue"
#             "must be one of the predefined category",
#         ),

#     )

#     priority: Priority = Field(

#         description = (
#             "The customers emotional sentiment expressed"
#             "In the support ticket",
#         )
#     )
#     Issue : str = Field(

#         description = (
#             "A concise description of the customers actual"
#             "Support issue",
#         ),
#     )
#     summary : str = Field(

#         min_length = 10,
#         description =(

#             "A concise business-friendly summary of the "
#             "Customer's problem"
#         ),
#     )

#     recommended_action : str= Field(
#         min_length = 10,
#         description = (
#             "A practical action that the support team should"
           
#             "take to reesolve or investigate the issue "
#         ),
#     )

# from typing import Literal

# from pydantic import BaseModel, Field

# class TicketAnalysis(BaseMopdel):
#     category: str = Field(

#         description=" The main category of the customers support issues."
#     )

# sentiment: Literal["positive", "negative", "neutral","frustrated","Angry"] = Field(

#     description = "The Customers emotional sentiment"
# )

# issue: str = Field(

#     description = "A Concise description of the customers main issue."
# )

# summary: str = Field(

#     description = "A concise Business-friendly summary of the ticket."
# )

# recommended_action: str = Field(

#     description = "The recommended action ther customer support team should take to resolve the issue."
# )
