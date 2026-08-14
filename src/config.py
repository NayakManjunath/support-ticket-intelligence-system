import os

from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please add it to your .env file."
    )


MODEL_NAME = "gemini-3.5-flash"

MAX_TICKETS = 10

REQUESTS_PER_MINUTE = 5

REQUEST_INTERVAL_SECONDS = 60 / REQUESTS_PER_MINUTE

MAX_RETRIES = 2

INPUT_FILE = "data/support_tickets.csv"

OUTPUT_FILE = "data/support_ticket_analysis.csv"

LOG_FILE = "data/support_ticket_system.log"

EVALUATION_TICKET_IDS = [
    "T001",
    "T002",
    "T004",
    "T005",
    "T006",
    "T007",
    "T010",
]