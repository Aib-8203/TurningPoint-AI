# TurningPoint AI

**Explainable AI-powered football match intelligence**

TurningPoint AI transforms synthetic football event data into understandable match insights. It detects significant changes in attacking activity, identifies the recorded events behind those changes, and uses Microsoft Foundry to explain them for different audiences.

Built as a solo submission for the **Microsoft × Premier League Inside the Game Hackathon 2026**.

## The Problem

Football statistics often show what happened without clearly explaining why a particular moment matters. TurningPoint AI bridges that gap by combining a transparent scoring algorithm with evidence-grounded AI explanations.

## Key Features

- **Attacking Activity Analysis:** Calculates weighted activity scores across 10-minute periods.
- **Turning Point Detection:** Flags significant increases in attacking activity.
- **Evidence-Based Explanations:** Connects AI-generated insights to recorded match events.
- **Casual Fan Mode:** Produces short, accessible football commentary.
- **Analyst Mode:** Provides detailed score comparisons, event IDs and limitations.
- **Interactive Dashboard:** Visualises attacking activity using Streamlit.

## Technology Stack

- Python
- Pandas
- Streamlit
- Microsoft Foundry
- OpenAI Python SDK
- Synthetic JSON football event data

## How It Works

1. **Ingest:** Load fictional football events from a JSON dataset.
2. **Interpret:** Assign weights to events and aggregate scores into 10-minute windows.
3. **Detect:** Identify increases above a configurable threshold.
4. **Explain:** Send the relevant event evidence to a model deployed through Microsoft Foundry.
5. **Personalise:** Generate different explanations for casual fans and analysts.

### Current Scoring Model

| Event | Weight |
|---|---:|
| Shot | 5 |
| Recovery | 3 |
| Pass | 1 |
| Foul | 0 |

The current turning-point threshold is 5 points.

These weights are illustrative design choices, not statistically validated measures of football performance.

## Running Locally

1. Clone the GitHub repository.
2. Install dependencies with `pip install -r requirements.txt`.
3. Configure `FOUNDRY_API_KEY`, `FOUNDRY_INFERENCE_BASE_URL` and `FOUNDRY_MODEL_NAME` as environment variables.
4. Start the application with `streamlit run app.py`.

Never commit credentials or API keys to this repository.

## Data and Limitations

All football events are synthetic and use fictional teams.

The model detects changes in **recorded weighted attacking activity**. These changes do not necessarily establish tactical superiority, sustained pressure or causal momentum shifts.

The current dataset is small, and results depend on the chosen event weights and detection threshold.

## Live Demo

**Streamlit App:** [Add deployment URL]

**Demonstration Video:** [Add public video URL]

## Future Improvements

- Larger football-realistic synthetic datasets
- Live-style event replay
- Side-by-side team comparison
- Additional match statistics and richer visualisations
- More robust evaluation of turning-point detection

## Project Status

Hackathon MVP — October 2026.
