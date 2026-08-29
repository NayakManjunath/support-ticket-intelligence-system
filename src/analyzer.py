import time

from google import genai

from src.config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    MAX_RETRIES,
    REQUEST_INTERVAL_SECONDS,
)
from src.logger import get_logger
from src.schemas import TicketAnalysis


client = genai.Client(
    api_key=GEMINI_API_KEY
)

logger = get_logger()

BASELINE_SYSTEM_INSTRUCTION = """
You are an expert customer support ticket analyst.

Your task is to analyze an unstructured customer support ticket
and convert it into structured, business-ready information.

============================================================
ALLOWED CATEGORIES
============================================================

You MUST select exactly ONE:

Password Reset
Payment Issue
Refund
Delivery
Account Access
Technical Issue
Order Issue
Billing
Subscription
Security
Other

Do not create new category names.

============================================================
PRIORITY
============================================================

Determine priority from the customer's actual urgency,
business impact, and potential consequences.

Low:
A minor request or inconvenience with limited impact.
No immediate action is required.

Medium:
A normal support issue that requires attention but does not
indicate immediate or significant impact.

High:
Use when there is clear urgency, significant customer impact,
financial impact, important service access problems, repeated
service failure, or a time-sensitive problem.

Critical:
Use only for severe security concerns, suspected account
compromise, or major immediate financial or operational impact.

IMPORTANT:
Do not assign High priority merely because the customer is
having a problem.

Do not assign Low priority merely because the customer is
asking a question.

Base priority on the actual facts and urgency expressed in
the ticket.

============================================================
SENTIMENT
============================================================

Select exactly ONE:

Positive:
The customer expresses satisfaction, appreciation, or a
clearly positive emotional tone.

Neutral:
The customer states a problem, request, or question without
strong emotional language.

Frustrated:
The customer expresses inconvenience, difficulty, annoyance,
repeated failure, or dissatisfaction, but not strong anger.

Angry:
The customer expresses strong anger, hostility, accusation,
outrage, or explicit anger.

Negative:
Use only when the emotional tone is clearly negative but
does not fit the more specific Frustrated or Angry categories.

IMPORTANT:
Do not classify a ticket as Angry simply because the customer
has a problem.

Do not classify a neutral request as Frustrated.

Use the emotional language actually present in the ticket.

============================================================
OUTPUT RULES
============================================================

1. Analyze only information present in the ticket.
2. Do not invent facts.
3. Select exactly one allowed category.
4. Select exactly one priority.
5. Select exactly one sentiment.
6. Keep the issue concise.
7. Keep the summary business-friendly.
8. Recommend a practical support action.
"""
IMPROVED_SYSTEM_INSTRUCTION = """
You are an expert customer support ticket analyst.

Your task is to analyze an unstructured customer support ticket
and convert it into structured, business-ready information.

============================================================
ALLOWED CATEGORIES
============================================================

You MUST select exactly ONE:

Password Reset
Payment Issue
Refund
Delivery
Account Access
Technical Issue
Order Issue
Billing
Subscription
Security
Other

Do not create new category names.

============================================================
PRIORITY
============================================================

Determine priority from the actual urgency, impact, and
consequences described in the ticket.

Low:
A minor request or inconvenience with limited impact.
No immediate action is required.

Medium:
A normal support issue that requires attention but does not
indicate immediate or significant impact.

High:
Use when there is clear urgency, significant customer impact,
financial impact, important service access problems, repeated
service failure, or a time-sensitive problem.

Critical:
Use only for severe security concerns, suspected account
compromise, or major immediate financial or operational impact.

IMPORTANT:
Do not assign High merely because the customer has a problem.

Do not assign Low merely because the customer is asking a
question.

Base priority on the actual facts and urgency expressed in
the ticket.

============================================================
SENTIMENT
============================================================

Select exactly ONE:

Positive:
The customer expresses satisfaction, appreciation, or a
clearly positive emotional tone.

Neutral:
The customer states a problem, request, or question without
strong emotional language.

Frustrated:
The customer expresses inconvenience, difficulty, annoyance,
repeated failure, or dissatisfaction, but not strong anger.

Angry:
The customer expresses strong anger, hostility, accusation,
outrage, or explicit anger.

Negative:
Use only when the emotional tone is clearly negative but does
not fit the more specific Frustrated or Angry categories.

IMPORTANT:
Do not classify a ticket as Angry simply because the customer
has a problem.

Do not classify a neutral request as Frustrated.

Use the emotional language actually present in the ticket.

============================================================
OUTPUT RULES
============================================================

1. Analyze only information present in the ticket.
2. Do not invent facts.
3. Select exactly one allowed category.
4. Select exactly one priority.
5. Select exactly one sentiment.
6. Keep the issue concise.
7. Keep the summary business-friendly.
8. Recommend a practical support action.
"""

_last_request_time = 0.0

def _is_daily_quota_error(error_text: str) -> bool:

    return (
        "GenerateRequestsPerDay" in error_text
        or "requests_per_day" in error_text.lower()
        or "daily quota" in error_text.lower()
    )

def _respect_rate_limit() -> None:
    """
    Prevent requests from exceeding the configured
    requests-per-minute limit.
    """

    global _last_request_time

    current_time = time.monotonic()

    elapsed = current_time - _last_request_time

    if elapsed < REQUEST_INTERVAL_SECONDS:
        wait_time = REQUEST_INTERVAL_SECONDS - elapsed

        logger.info(
            "Rate limit protection: waiting %.1f seconds",
            wait_time,
        )

        time.sleep(wait_time)

    _last_request_time = time.monotonic()


def analyze_ticket(
    ticket_text: str,
    prompt_version: str = "baseline",
) -> TicketAnalysis:

    if prompt_version == "baseline":

        system_instruction = (
            BASELINE_SYSTEM_INSTRUCTION
        )

    elif prompt_version == "improved":

        system_instruction = (
            IMPROVED_SYSTEM_INSTRUCTION
        )

    else:

        raise ValueError(
            f"Unsupported prompt version: "
            f"{prompt_version}"
        )

    prompt = f"""
{system_instruction}

============================================================
CUSTOMER SUPPORT TICKET
============================================================

{ticket_text}

============================================================
TASK
============================================================

Analyze this ticket and return the structured result.
"""

    for attempt in range(MAX_RETRIES + 1):

        try:

            _respect_rate_limit()

            logger.info(
                "Sending ticket to Gemini | attempt=%d",
                attempt + 1,
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema":
                        TicketAnalysis.model_json_schema(),
                },
            )

            result = TicketAnalysis.model_validate_json(
                response.text
            )

            logger.info(
                "Gemini analysis successful"
            )

            return result

        except Exception as error:

            error_text = str(error)

            is_rate_limit_error = (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            )

            # ----------------------------------------------------------
            # Daily quota exhausted
            # Retrying will not help during the current quota window.
            # ----------------------------------------------------------

            if (
                is_rate_limit_error
                and _is_daily_quota_error(error_text)
            ):

                logger.error(
                    "Daily Gemini API quota exhausted. "
                    "Stopping retries."
                )

                raise

            # ----------------------------------------------------------
            # Temporary rate limit
            # Retry only if we have attempts remaining.
            # ----------------------------------------------------------

            if (
                is_rate_limit_error
                and attempt < MAX_RETRIES
            ):

                retry_wait = 45 * (attempt + 1)

                logger.warning(
                    "Temporary rate limit encountered. "
                    "Retrying in %d seconds | attempt=%d",
                    retry_wait,
                    attempt + 1,
                )

                time.sleep(retry_wait)

                continue

            logger.error(
                "Gemini analysis failed | attempt=%d | error=%s",
                attempt + 1,
                error,
            )

            raise
        
def _is_daily_quota_error(error_text: str) -> bool:

    return (
        "GenerateRequestsPerDay" in error_text
        or "requests_per_day" in error_text.lower()
        or "daily quota" in error_text.lower()
    )
