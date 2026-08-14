import pandas as pd


EVALUATION_FIELDS = [
    "category",
    "priority",
    "sentiment",
]


CATEGORY_MAPPING = {
    "Password Reset": "Password Reset",
    "Payment": "Payment Issue",
    "Account": "Account Access",
    "Technical Issue": "Technical Issue",
    "Delivery": "Delivery",
    "Refund": "Refund",
    "Login": "Account Access",
    "Billing": "Billing",
    "Subscription": "Subscription",
}

def prepare_ground_truth(
    source_data: pd.DataFrame,
    ticket_ids=None,
) -> pd.DataFrame:

    required_columns = {
        "ticket_id",
        "known_category",
        "known_priority",
        "known_sentiment",
    }

    missing_columns = (
        required_columns - set(source_data.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing ground-truth columns: {missing_columns}"
        )

    ground_truth = source_data[
        [
            "ticket_id",
            "known_category",
            "known_priority",
            "known_sentiment",
        ]
    ].copy()

    # ----------------------------------------------------------
    # Only evaluate tickets for which predictions exist.
    # This is important because the source dataset may contain
    # more tickets than were sent to the API.
    # ----------------------------------------------------------

    if ticket_ids is not None:

        ground_truth = ground_truth[
            ground_truth["ticket_id"].isin(ticket_ids)
        ].copy()

    ground_truth["category"] = (
        ground_truth["known_category"]
        .map(CATEGORY_MAPPING)
    )

    if ground_truth["category"].isna().any():

        unknown_categories = (
            ground_truth.loc[
                ground_truth["category"].isna(),
                "known_category",
            ]
            .unique()
            .tolist()
        )

        raise ValueError(
            "Unknown source categories found: "
            f"{unknown_categories}"
        )

    ground_truth["priority"] = (
        ground_truth["known_priority"]
    )

    ground_truth["sentiment"] = (
        ground_truth["known_sentiment"]
    )

    return ground_truth[
        [
            "ticket_id",
            "category",
            "priority",
            "sentiment",
        ]
    ]

def create_error_analysis(
    predictions: pd.DataFrame,
    source_data: pd.DataFrame,
) -> pd.DataFrame:

    ground_truth = prepare_ground_truth(
        source_data,
        ticket_ids=predictions["ticket_id"],
    )

    merged = ground_truth.merge(
        predictions,
        on="ticket_id",
        suffixes=("_expected", "_predicted"),
        how="inner",
    )

    if merged.empty:
        raise ValueError(
            "No matching ticket IDs found between "
            "source data and predictions."
        )

    for field in EVALUATION_FIELDS:

        expected_column = f"{field}_expected"
        predicted_column = f"{field}_predicted"
        correct_column = f"{field}_correct"

        merged[correct_column] = (
            merged[expected_column]
            == merged[predicted_column]
        )

    error_columns = [
        "ticket_id",

        "category_expected",
        "category_predicted",
        "category_correct",

        "priority_expected",
        "priority_predicted",
        "priority_correct",

        "sentiment_expected",
        "sentiment_predicted",
        "sentiment_correct",
    ]

    return merged[error_columns]


def calculate_accuracy(
    predictions: pd.DataFrame,
    source_data: pd.DataFrame,
) -> dict:

    error_analysis = create_error_analysis(
        predictions,
        source_data,
    )

    metrics = {}

    total_correct = 0
    total_fields = 0

    total_tickets = len(error_analysis)

    for field in EVALUATION_FIELDS:

        correct_column = f"{field}_correct"

        correct = int(
            error_analysis[correct_column].sum()
        )

        accuracy = correct / total_tickets

        metrics[f"{field}_accuracy"] = round(
            accuracy * 100,
            2,
        )

        total_correct += correct
        total_fields += total_tickets

    metrics["overall_field_accuracy"] = round(
        (total_correct / total_fields) * 100,
        2,
    )

    metrics["tickets_evaluated"] = total_tickets

    return metrics

