# Support Ticket Intelligence System

A mini portfolio project that uses Generative AI to transform unstructured customer-support tickets into structured, actionable business data.

Built with **Python, Gemini API, Pydantic, Pandas, Pytest, and Git**.

---

## Overview

Customer-support teams receive large volumes of tickets covering password issues, payment failures, refunds, delivery delays, account problems, billing questions, subscriptions, and technical issues.

Manually reading and classifying every ticket is time-consuming and can lead to inconsistent prioritization.

This project automates the first level of support-ticket intelligence by converting unstructured ticket text into validated structured information.

### Pipeline

```text
Customer Support Ticket
        |
        v
   CSV Dataset
        |
        v
    Gemini API
        |
        v
Structured Pydantic Model
        |
        v
     Validation
        |
        v
 Business-Ready CSV
        |
        v
Evaluation & Error Analysis
        |
        v
Prompt Improvement Experiment
```

For each ticket, the system extracts:

- Ticket ID
- Category
- Priority
- Sentiment
- Issue
- Summary
- Recommended Action

---

## Example

### Input

**Ticket ID:** `T001`

> I cannot reset my password. The reset link says it has expired.

### Structured Output

| Field | Result |
|---|---|
| Category | Password Reset |
| Priority | High |
| Sentiment | Frustrated |
| Issue | Password reset link has expired |
| Summary | Customer is unable to reset their password. |
| Recommended Action | Assist the customer with resetting their password. |

---

## Key Features

### 1. GenAI-powered ticket analysis

Gemini analyzes unstructured ticket text and extracts structured business information.

### 2. Structured output validation

Pydantic validates the Gemini response before it is written to the final dataset.

### 3. Controlled taxonomy

Ticket categories, priorities, and sentiment values are constrained using predefined taxonomy rules.

### 4. API reliability

The pipeline includes:

- Rate-limit protection
- Retry handling
- Temporary API failure handling
- Daily quota detection
- Logging
- Graceful failure handling

For the free Gemini API, processing is intentionally limited to a small number of tickets per run.

### 5. Evaluation pipeline

The system compares model predictions against labeled ticket data and calculates:

- Category accuracy
- Priority accuracy
- Sentiment accuracy
- Overall field accuracy

### 6. Error analysis

Incorrect predictions are analyzed at both ticket and field level to identify systematic weaknesses.

### 7. Prompt improvement experiment

A second prompt version was created using baseline error analysis to specifically target priority and sentiment classification issues.

---

## Project Structure

```text
support_ticket_intilegence_system/
|
├── data/
│   ├── support_tickets.csv
│   ├── support_ticket_analysis.csv
│   ├── evaluation_results.csv
│   └── evaluation_error_analysis.csv
|
├── experiments/
│   └── support_ticket_analysis_v2.csv
|
├── src/
│   ├── analyzer.py
│   ├── config.py
│   ├── evaluator.py
│   ├── logger.py
│   ├── main.py
│   ├── run_evaluation.py
│   ├── run_experiment.py
│   ├── schemas.py
│   └── taxonomy.py
|
├── test/
│   ├── test_analyzer.py
│   ├── test_evaluator.py
│   └── test_schemas.py
|
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Evaluation

The baseline system was evaluated against **10 labeled support tickets**.

| Metric | Result |
|---|---:|
| Category Accuracy | **100.0%** |
| Priority Accuracy | **50.0%** |
| Sentiment Accuracy | **70.0%** |
| Overall Field Accuracy | **73.33%** |

### Interpretation

The system performed strongly on category classification.

However, **priority classification was the main weakness**, followed by sentiment classification.

This demonstrates why evaluation is important for GenAI systems: a successful API response does not necessarily mean the prediction is correct.

---

## Error Analysis

The baseline evaluation identified:

**Tickets with at least one error: 7 / 10**

### Priority

**5 priority classification errors** were identified.

| Ticket | Predicted | Expected |
|---|---|---|
| T001 | Medium | High |
| T004 | Medium | High |
| T005 | Medium | High |
| T006 | Low | Medium |
| T010 | High | Medium |

### Sentiment

**3 sentiment classification errors** were identified.

| Ticket | Predicted | Expected |
|---|---|---|
| T001 | Neutral | Frustrated |
| T002 | Negative | Angry |
| T007 | Neutral | Frustrated |

### Category

Category classification achieved:

**100% accuracy**

No category errors were identified in the evaluated dataset.

---

## Prompt Improvement Experiment

Based on the baseline error analysis, an improved prompt version was implemented with stronger instructions around priority and sentiment interpretation.

The experiment reused the same tickets that failed in the baseline evaluation:

```text
T001, T002, T004, T005, T006, T007, T010
```

One successful V2 result was produced for **T010**:

| Field | Baseline | V2 | Expected |
|---|---|---|---|
| Category | Subscription | Subscription | Subscription |
| Priority | High | Medium | Medium |
| Sentiment | Neutral | Neutral | Neutral |

The V2 prompt successfully corrected the priority classification for T010.

The complete V2 experiment could not be completed because the Gemini API subsequently returned temporary `503 UNAVAILABLE` responses.

Therefore, **no overall V2 accuracy claim is made**.

This is intentionally documented rather than presenting an incomplete experiment as a full evaluation.

---

## Reliability Engineering

The project was designed to handle common API failure scenarios.

```text
                    Gemini API Request
                           |
          +----------------+----------------+
          |                |                |
       Success            429              503
          |             Temporary        Temporary
          v                |                |
       Validate            v                v
                         Retry         Retry / Stop
          |
          v
      Save Result

          Daily Quota
               |
               v
              Stop

     Validation Error
               |
               v
              Fail
```

The system also logs API activity, processing status, retries, and failures.

---

## Testing

The project uses **Pytest** for automated testing.

Current test coverage includes:

- Pydantic schema validation
- Valid ticket analysis
- Invalid category handling
- Invalid priority handling
- Invalid sentiment handling
- Analyzer behavior
- Evaluation calculations
- Error-analysis logic

### Current Test Result

```text
11 passed
```

Run the tests with:

```powershell
pytest
```

---

## Installation

### 1. Clone the repository

```powershell
git clone <your-repository-url>
cd support_ticket_intilegence_system
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root.

Use `.env.example` as the template:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Never commit `.env` to Git.**

The project keeps the Gemini API key outside the source code through environment configuration.

---

## Run the System

Run the main ticket-analysis pipeline:

```powershell
python -m src.main
```

The analyzed tickets are written to:

```text
data/support_ticket_analysis.csv
```

The free API configuration limits each run to a small number of tickets.

---

## Run Evaluation

Run:

```powershell
python -m src.run_evaluation
```

This generates:

```text
data/evaluation_results.csv
data/evaluation_error_analysis.csv
```

---

## Run the Prompt Experiment

Run:

```powershell
python -m src.run_experiment
```

The experiment uses the tickets identified by the baseline error analysis and writes successful V2 results to:

```text
experiments/support_ticket_analysis_v2.csv
```

Because the free Gemini API has quota and availability limitations, the experiment may not complete for every selected ticket.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| Gemini API | Generative AI analysis |
| Pydantic | Structured output validation |
| Pandas | Dataset processing |
| Pytest | Automated testing |
| python-dotenv | Environment configuration |
| Logging | Application observability |
| Git | Version control |

---

## Design Decisions

### Why Gemini?

The project focuses on applying a production-oriented LLM workflow to an unstructured text classification problem.

### Why Pydantic?

LLM output is probabilistic.

Pydantic provides a validation layer between the model response and downstream business logic:

```text
Gemini
  |
  v
Pydantic
  |
  v
Validated Structure
  |
  v
CSV
```

This prevents malformed or invalid model output from silently entering the downstream dataset.

### Why evaluate individual fields?

A single overall accuracy number can hide important weaknesses.

For example, this project achieved:

```text
Category:  100%
Priority:   50%
Sentiment:  70%
```

Field-level evaluation made the priority classification problem immediately visible.

---

## Limitations

This is a **mini portfolio project** and intentionally keeps the architecture simple.

Current limitations include:

- Evaluation is based on a small labeled dataset.
- The free Gemini API imposes request and quota limitations.
- The V2 prompt experiment could not be completed for all selected tickets because of Gemini API availability.
- No human-in-the-loop review interface is implemented.
- No database or production deployment infrastructure is included.

These limitations would need to be addressed before using the system in a high-volume production support environment.

---

## Future Improvements

Potential production extensions include:

- Larger human-labeled evaluation datasets
- Confidence scoring
- Human review for low-confidence predictions
- Batch inference
- Persistent storage
- FastAPI service
- Monitoring and model-quality dashboards
- Prompt/version tracking
- Automated regression evaluation
- Cost and latency monitoring

These improvements are intentionally outside the scope of this mini portfolio implementation.

---

## What This Project Demonstrates

This project demonstrates a complete evaluation-driven GenAI application workflow:

```text
Unstructured Data
       |
       v
LLM Analysis
       |
       v
Structured Output
       |
       v
Validation
       |
       v
Business Output
       |
       v
Automated Testing
       |
       v
Evaluation
       |
       v
Error Analysis
       |
       v
Prompt Improvement
       |
       v
Reliability Handling
```

The focus is not simply on calling an LLM API.

It demonstrates how to build a small but structured GenAI system around the model with:

- Schema validation
- Controlled outputs
- Reliability handling
- Automated tests
- Quantitative evaluation
- Field-level error analysis
- Prompt iteration
- Honest experiment reporting

---

## Author

**Manjunath Nayak**

Data Scientist | Generative AI | Machine Learning | Python
