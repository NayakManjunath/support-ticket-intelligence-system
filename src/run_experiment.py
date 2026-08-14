import pandas as pd

from src.analyzer import analyze_ticket
from src.logger import get_logger


SOURCE_FILE = "data/support_tickets.csv"

BASELINE_FILE = "data/support_ticket_analysis.csv"

EXPERIMENT_FILE = (
    "data/support_ticket_analysis_v2.csv"
)

ERROR_ANALYSIS_FILE = (
    "data/evaluation_error_analysis.csv"
)


EXPERIMENT_TICKET_IDS = [
    "T001",
    "T002",
    "T004",
    "T005",
    "T006",
    "T007",
    "T010",
]


logger = get_logger()


def load_experiment_tickets():

    source_data = pd.read_csv(
        SOURCE_FILE
    )

    tickets = source_data[
        source_data["ticket_id"].isin(
            EXPERIMENT_TICKET_IDS
        )
    ].copy()

    if len(tickets) != len(
        EXPERIMENT_TICKET_IDS
    ):

        found_ids = set(
            tickets["ticket_id"]
        )

        missing_ids = (
            set(EXPERIMENT_TICKET_IDS)
            - found_ids
        )

        raise ValueError(
            "Some experiment ticket IDs "
            f"were not found: {sorted(missing_ids)}"
        )

    # Preserve the requested experiment order
    tickets["ticket_order"] = (
        tickets["ticket_id"].map(
            {
                ticket_id: index
                for index, ticket_id
                in enumerate(EXPERIMENT_TICKET_IDS)
            }
        )
    )

    tickets = tickets.sort_values(
        "ticket_order"
    )

    return tickets


def main():

    print("=" * 70)
    print("PROMPT IMPROVEMENT EXPERIMENT")
    print("=" * 70)

    print(
        "\nExperiment tickets:"
    )

    print(
        ", ".join(EXPERIMENT_TICKET_IDS)
    )

    print(
        "\nThese are the same 7 tickets "
        "identified by the baseline error analysis."
    )

    tickets = load_experiment_tickets()

    results = []

    for _, row in tickets.iterrows():

        ticket_id = str(
            row["ticket_id"]
        ).strip()

        ticket_text = str(
            row["ticket_text"]
        ).strip()

        print("\n" + "-" * 70)
        print(
            f"Processing experiment ticket: "
            f"{ticket_id}"
        )

        logger.info(
            "Experiment processing | ticket_id=%s",
            ticket_id,
        )

        try:

            analysis = analyze_ticket(
                ticket_text,
                prompt_version="improved",
            )

            result = {
                "ticket_id": ticket_id,
                "category": analysis.category,
                "priority": analysis.priority,
                "sentiment": analysis.sentiment,
                "issue": analysis.issue,
                "summary": analysis.summary,
                "recommended_action": (
                    analysis.recommended_action
                ),
            }

            results.append(result)

            print("Status: SUCCESS")
            print(
                f"Category: {analysis.category}"
            )
            print(
                f"Priority: {analysis.priority}"
            )
            print(
                f"Sentiment: {analysis.sentiment}"
            )

        except Exception as error:

                    print("Status: FAILED")
                    print(f"Error: {error}")

                    logger.error(
                        "Experiment failed | "
                        "ticket_id=%s | error=%s",
                        ticket_id,
                        error,
                    )

                    error_text = str(error)

                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                        or "GenerateRequestsPerDay" in error_text
                        or "daily quota" in error_text.lower()
                    ):

                        print("\n" + "=" * 70)
                        print("EXPERIMENT STOPPED")
                        print("=" * 70)

                        print(
                            "\nGemini API is temporarily unavailable "
                            "or the daily quota is exhausted."
                        )

                        print(
                            "The experiment has been stopped to avoid "
                            "unnecessary API requests."
                        )

                        break
    if not results:

        print("\n" + "=" * 70)
        print("EXPERIMENT FAILED")
        print("=" * 70)

        print(
            "\nNo tickets were successfully analyzed."
        )

        return

    output_columns = [
        "ticket_id",
        "category",
        "priority",
        "sentiment",
        "issue",
        "summary",
        "recommended_action",
    ]

    output_df = pd.DataFrame(
        results,
        columns=output_columns,
    )

    output_df.to_csv(
        EXPERIMENT_FILE,
        index=False,
    )

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)

    print(
        f"\nSuccessfully analyzed: "
        f"{len(results)} / "
        f"{len(EXPERIMENT_TICKET_IDS)}"
    )

    print(
        f"Experiment output: "
        f"{EXPERIMENT_FILE}"
    )


if __name__ == "__main__":
    main()