import pandas as pd

from src.analyzer import analyze_ticket
from src.config import (
    INPUT_FILE,
    MAX_TICKETS,
    OUTPUT_FILE,
)
from src.logger import get_logger


logger = get_logger()


def main():

    print("=" * 70)
    print("SUPPORT TICKET INTELLIGENCE SYSTEM")
    print("=" * 70)

    print(f"\nReading Dataset: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)

    logger.info(
        "Dataset loaded | total_tickets=%d",
        len(df),
    )

    print(
        f"\nTotal Tickets in Dataset: {len(df)}"
    )

    required_columns = {
        "ticket_id",
        "ticket_text",
    }

    missing_columns = (
        required_columns - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Free API protection
    df = df.head(MAX_TICKETS).copy()

    print(
        f"\nTickets selected for Gemini analysis: "
        f"{len(df)}\n"
    )

    results = []

    for _, row in df.iterrows():

        ticket_id = str(row["ticket_id"]).strip()
        ticket_text = str(row["ticket_text"]).strip()

        print("-" * 70)
        print(f"Processing ticket: {ticket_id}")

        logger.info(
            "Processing ticket | ticket_id=%s",
            ticket_id,
        )

        if not ticket_id:

            logger.warning(
                "Skipping ticket with missing ticket ID"
            )

            print("Status: SKIPPED")
            print("Reason: Missing ticket ID")

            continue

        if not ticket_text:

            logger.warning(
                "Skipping ticket with empty ticket text | "
                "ticket_id=%s",
                ticket_id,
            )

            print("Status: SKIPPED")
            print("Reason: Empty ticket text")

            continue

        try:

            analysis = analyze_ticket(
                ticket_text
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

            logger.info(
                "Ticket completed successfully | "
                "ticket_id=%s",
                ticket_id,
            )

        except Exception as error:

            print("Status: FAILED")
            print(f"Error: {error}")

            logger.error(
                "Ticket failed | ticket_id=%s | error=%s",
                ticket_id,
                error,
            )

            # Continue processing remaining tickets
            continue

    # ==========================================================
    # OUTPUT SECTION
    # IMPORTANT: THIS IS OUTSIDE THE FOR LOOP
    # ==========================================================

    output_columns = [
        "ticket_id",
        "category",
        "priority",
        "sentiment",
        "issue",
        "summary",
        "recommended_action",
    ]

    if not results:

        print("\n" + "=" * 70)
        print("NO TICKETS WERE SUCCESSFULLY ANALYZED")
        print("=" * 70)

        logger.warning(
            "Pipeline completed with zero successful tickets"
        )

        return

    output_df = pd.DataFrame(
        results,
        columns=output_columns,
    )

    output_df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    # ==========================================================
    # FINAL SUMMARY
    # IMPORTANT: THIS IS ALSO OUTSIDE THE FOR LOOP
    # ==========================================================

    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)

    print(
        f"\nSuccessfully analyzed: "
        f"{len(results)} tickets"
    )

    print(
        f"Output file: {OUTPUT_FILE}"
    )

    logger.info(
        "Pipeline completed | successful_tickets=%d",
        len(results),
    )


if __name__ == "__main__":
    main()
