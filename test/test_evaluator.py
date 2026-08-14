import pandas as pd

from src.evaluator import calculate_accuracy


def test_perfect_accuracy():

    source_data = pd.DataFrame(
        {
            "ticket_id": ["T001", "T002"],
            "known_category": [
                "Password Reset",
                "Payment",
            ],
            "known_priority": [
                "Medium",
                "High",
            ],
            "known_sentiment": [
                "Neutral",
                "Frustrated",
            ],
        }
    )

    predictions = pd.DataFrame(
        {
            "ticket_id": ["T001", "T002"],
            "category": [
                "Password Reset",
                "Payment Issue",
            ],
            "priority": [
                "Medium",
                "High",
            ],
            "sentiment": [
                "Neutral",
                "Frustrated",
            ],
        }
    )

    metrics = calculate_accuracy(
        predictions,
        source_data,
    )

    assert metrics["category_accuracy"] == 100.0
    assert metrics["priority_accuracy"] == 100.0
    assert metrics["sentiment_accuracy"] == 100.0
    assert metrics["overall_field_accuracy"] == 100.0


def test_partial_accuracy():

    source_data = pd.DataFrame(
        {
            "ticket_id": ["T001", "T002"],
            "known_category": [
                "Password Reset",
                "Payment",
            ],
            "known_priority": [
                "Medium",
                "High",
            ],
            "known_sentiment": [
                "Neutral",
                "Frustrated",
            ],
        }
    )

    predictions = pd.DataFrame(
        {
            "ticket_id": ["T001", "T002"],
            "category": [
                "Password Reset",
                "Payment Issue",
            ],
            "priority": [
                "Low",
                "High",
            ],
            "sentiment": [
                "Neutral",
                "Negative",
            ],
        }
    )


def test_error_analysis_identifies_incorrect_fields():

    source_data = pd.DataFrame(
        {
            "ticket_id": ["T001"],
            "known_category": ["Payment"],
            "known_priority": ["High"],
            "known_sentiment": ["Frustrated"],
        }
    )

    predictions = pd.DataFrame(
        {
            "ticket_id": ["T001"],
            "category": ["Payment Issue"],
            "priority": ["Low"],
            "sentiment": ["Neutral"],
        }
    )

    from src.evaluator import create_error_analysis

    result = create_error_analysis(
        predictions,
        source_data,
    )

    assert len(result) == 1

    assert result.loc[
        0, "category_correct"
    ]

    assert not result.loc[
        0, "priority_correct"
    ]

    assert not result.loc[
        0, "sentiment_correct"
    ]


def test_error_analysis_all_correct():

    source_data = pd.DataFrame(
        {
            "ticket_id": ["T001"],
            "known_category": ["Payment"],
            "known_priority": ["High"],
            "known_sentiment": ["Frustrated"],
        }
    )

    predictions = pd.DataFrame(
        {
            "ticket_id": ["T001"],
            "category": ["Payment Issue"],
            "priority": ["High"],
            "sentiment": ["Frustrated"],
        }
    )

    from src.evaluator import create_error_analysis

    result = create_error_analysis(
        predictions,
        source_data,
    )

    assert result.loc[
        0, "category_correct"
    ]

    assert result.loc[
        0, "priority_correct"
    ]

    assert result.loc[
        0, "sentiment_correct"
    ]

    metrics = calculate_accuracy(
        predictions,
        source_data,
    )

    assert metrics["category_accuracy"] == 100.0
    assert metrics["priority_accuracy"] == 100.0
    assert metrics["sentiment_accuracy"] == 100.0
    assert metrics["overall_field_accuracy"] == 100.0