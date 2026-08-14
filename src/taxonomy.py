from typing import Literal


Category = Literal[
    "Password Reset",
    "Payment Issue",
    "Refund",
    "Delivery",
    "Account Access",
    "Technical Issue",
    "Order Issue",
    "Billing",
    "Subscription",
    "Security",
    "Other",
]


Priority = Literal[
    "Low",
    "Medium",
    "High",
    "Critical",
]


Sentiment = Literal[
    "Positive",
    "Neutral",
    "Frustrated",
    "Angry",
    "Negative",
]
