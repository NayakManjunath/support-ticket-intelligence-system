import pytest
from pydantic import ValidationError

from src.schemas import TicketAnalysis


def test_valid_ticket_analysis():

    result = TicketAnalysis(
        category="Payment Issue",
        priority="High",
        sentiment="Frustrated",
        issue="Customer was charged twice for the same order.",
        summary="Customer reports a duplicate payment.",
        recommended_action=(
            "Verify the duplicate transaction and initiate "
            "a refund if confirmed."
        ),
    )

    assert result.category == "Payment Issue"
    assert result.priority == "High"
    assert result.sentiment == "Frustrated"


def test_invalid_category():

    with pytest.raises(ValidationError):

        TicketAnalysis(
            category="Duplicate Payment",
            priority="High",
            sentiment="Frustrated",
            issue="Customer was charged twice.",
            summary="Customer reports a duplicate charge.",
            recommended_action=(
                "Investigate the duplicate transaction."
            ),
        )


def test_invalid_priority():

    with pytest.raises(ValidationError):

        TicketAnalysis(
            category="Payment Issue",
            priority="Very High",
            sentiment="Frustrated",
            issue="Customer was charged twice.",
            summary="Customer reports a duplicate charge.",
            recommended_action=(
                "Investigate the duplicate transaction."
            ),
        )


def test_invalid_sentiment():

    with pytest.raises(ValidationError):

        TicketAnalysis(
            category="Payment Issue",
            priority="High",
            sentiment="Very Angry",
            issue="Customer was charged twice.",
            summary="Customer reports a duplicate charge.",
            recommended_action=(
                "Investigate the duplicate transaction."
            ),
        )