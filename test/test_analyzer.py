from unittest.mock import MagicMock, patch

import pytest

from src.analyzer import analyze_ticket
from src.schemas import TicketAnalysis


def valid_response():

    response = MagicMock()

    response.text = """
    {
        "category": "Payment Issue",
        "priority": "High",
        "sentiment": "Frustrated",
        "issue": "Customer was charged twice.",
        "summary": "Customer reports a duplicate payment.",
        "recommended_action": "Verify the duplicate transaction."
    }
    """

    return response


@patch("src.analyzer.client")
@patch("src.analyzer._respect_rate_limit")
def test_successful_analysis(
    mock_rate_limit,
    mock_client,
):

    mock_client.models.generate_content.return_value = (
        valid_response()
    )

    result = analyze_ticket(
        "My card was charged twice."
    )

    assert isinstance(
        result,
        TicketAnalysis,
    )

    assert result.category == "Payment Issue"

    mock_client.models.generate_content.assert_called_once()


@patch("src.analyzer.time.sleep")
@patch("src.analyzer.client")
@patch("src.analyzer._respect_rate_limit")
def test_rate_limit_retry(
    mock_rate_limit,
    mock_client,
    mock_sleep,
):

    rate_limit_error = Exception(
        "429 RESOURCE_EXHAUSTED"
    )

    mock_client.models.generate_content.side_effect = [
        rate_limit_error,
        valid_response(),
    ]

    result = analyze_ticket(
        "My card was charged twice."
    )

    assert result.category == "Payment Issue"

    assert (
        mock_client.models.generate_content.call_count
        == 2
    )

    mock_sleep.assert_called_once_with(45)


@patch("src.analyzer.client")
@patch("src.analyzer._respect_rate_limit")
def test_permanent_failure(
    mock_rate_limit,
    mock_client,
):

    mock_client.models.generate_content.side_effect = (
        Exception("500 Internal Server Error")
    )

    with pytest.raises(Exception):

        analyze_ticket(
            "My application is crashing."
        )

    assert (
        mock_client.models.generate_content.call_count
        == 1
    )