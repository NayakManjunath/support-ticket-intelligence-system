import pandas as pd

from src.evaluator import (
    calculate_accuracy,
    create_error_analysis,
)


SOURCE_FILE = (
    "data/support_tickets.csv"
)

PREDICTIONS_FILE = (
    "data/support_ticket_analysis.csv"
)

RESULTS_FILE = (
    "data/evaluation_results.csv"
)

ERROR_ANALYSIS_FILE = (
    "data/evaluation_error_analysis.csv"
)


def main():

    print("=" * 70)
    print("SUPPORT TICKET EVALUATION")
    print("=" * 70)

    source_data = pd.read_csv(
        SOURCE_FILE
    )

    predictions = pd.read_csv(
        PREDICTIONS_FILE
    )

    metrics = calculate_accuracy(
        predictions,
        source_data,
    )

    error_analysis = create_error_analysis(
        predictions,
        source_data,
    )

    print("\nEvaluation Results")
    print("-" * 70)

    print(
        f"Tickets evaluated: "
        f"{metrics['tickets_evaluated']}"
    )

    print(
        f"Category Accuracy: "
        f"{metrics['category_accuracy']}%"
    )

    print(
        f"Priority Accuracy: "
        f"{metrics['priority_accuracy']}%"
    )

    print(
        f"Sentiment Accuracy: "
        f"{metrics['sentiment_accuracy']}%"
    )

    print(
        f"Overall Field Accuracy: "
        f"{metrics['overall_field_accuracy']}%"
    )

    # Save metrics
    pd.DataFrame(
        [metrics]
    ).to_csv(
        RESULTS_FILE,
        index=False,
    )

    # Keep only tickets with at least
    # one incorrect prediction.
    errors_only = error_analysis[
        ~(
            error_analysis[
                [
                    "category_correct",
                    "priority_correct",
                    "sentiment_correct",
                ]
            ].all(axis=1)
        )
    ].copy()

    errors_only.to_csv(
        ERROR_ANALYSIS_FILE,
        index=False,
    )

    print(
        f"\nTickets with at least one error: "
        f"{len(errors_only)}"
    )

    print(
        f"Evaluation saved to: {RESULTS_FILE}"
    )

    print(
        f"Error analysis saved to: "
        f"{ERROR_ANALYSIS_FILE}"
    )

    if not errors_only.empty:

        print("\nError Analysis")
        print("-" * 70)

        for _, row in errors_only.iterrows():

            print(
                f"\nTicket: {row['ticket_id']}"
            )

            if not row["category_correct"]:

                print(
                    "  Category: "
                    f"{row['category_predicted']} "
                    f"(expected: "
                    f"{row['category_expected']})"
                )

            if not row["priority_correct"]:

                print(
                    "  Priority: "
                    f"{row['priority_predicted']} "
                    f"(expected: "
                    f"{row['priority_expected']})"
                )

            if not row["sentiment_correct"]:

                print(
                    "  Sentiment: "
                    f"{row['sentiment_predicted']} "
                    f"(expected: "
                    f"{row['sentiment_expected']})"
                )


if __name__ == "__main__":
    main()

# import pandas as pd

# from src.evaluator import calculate_accuracy


# SOURCE_FILE = (
#     "data/support_tickets.csv"
# )

# PREDICTIONS_FILE = (
#     "data/support_ticket_analysis.csv"
# )

# OUTPUT_FILE = (
#     "data/evaluation_results.csv"
# )


# def main():

#     print("=" * 70)
#     print("SUPPORT TICKET EVALUATION")
#     print("=" * 70)

#     source_data = pd.read_csv(
#         SOURCE_FILE
#     )

#     predictions = pd.read_csv(
#         PREDICTIONS_FILE
#     )

#     metrics = calculate_accuracy(
#         predictions,
#         source_data,
#     )

#     print("\nEvaluation Results")
#     print("-" * 70)

#     print(
#         f"Tickets evaluated: "
#         f"{metrics['tickets_evaluated']}"
#     )

#     print(
#         f"Category Accuracy: "
#         f"{metrics['category_accuracy']}%"
#     )

#     print(
#         f"Priority Accuracy: "
#         f"{metrics['priority_accuracy']}%"
#     )

#     print(
#         f"Sentiment Accuracy: "
#         f"{metrics['sentiment_accuracy']}%"
#     )

#     print(
#         f"Overall Field Accuracy: "
#         f"{metrics['overall_field_accuracy']}%"
#     )

#     results_df = pd.DataFrame(
#         [metrics]
#     )

#     results_df.to_csv(
#         OUTPUT_FILE,
#         index=False,
#     )

#     print(
#         f"\nEvaluation saved to: "
#         f"{OUTPUT_FILE}"
#     )


# if __name__ == "__main__":
#     main()