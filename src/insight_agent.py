
import os
import json

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def explain_turning_point(turning_point, previous_events, current_events, audience):
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model_name = os.environ["FOUNDRY_MODEL_NAME"]

    project = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    )

    client = project.get_openai_client()

    current_json = json.dumps(current_events)
    previous_json = json.dumps(previous_events)
    instructions = json.dumps(audience)


    if audience == "Casual Fan":
      instructions = """Explain the match situation like a fottball commentator in two short,
    engaging sentences using everyday football language.
    Avoid technical terms and detailed calculations.
    Mention key recorded events naturally.
    Don't reference anything technical including event id's and complex language from data.
    Don't invent tactical explanations or claim
    the momentum shift will continue.
    Instead of event mention the period/ minutes in which it took place.
    """

    elif audience == "Analyst":
      instructions = "Explain using more detailed, with score differences, specific event IDs and limitations."
    else:
      instructions = "Explain clearly using only the evidence."

    
    prompt = f"""
    You are TurningPoint AI, an explainable football analyst.

    
    Our weighted attacking activity score:
    - Shot = 5 points
    - Recovery = 3 points
    - Pass = 1 point
    - Foul = 0 points


    Previous attacking score: {turning_point["previous_score"]}
    Current attacking score: {turning_point["score"]}

    Previous period events:
    {previous_json}

    Current period events:
    {current_json}

    Audience instructions:
    {instructions}

    Instructions:
    - Compare attacking activity between both periods.
    - Explain which recorded events contributed to the scores.
    - Do not invent events, players or tactical causes.
    - Explain uncertainties when evidence is insufficient.
    - Keep your explanation concise.
    - When explaining an event, reference its event_id.
    - Only reference event IDs present in the provided data.
    - Do not claim that a momentum shift proves a tactical change.
    - The supplied events are filtered to the selected team.
    - Do not make claims about the opposing team's activity.
    - Distinguish detected changes in weighted attacking
    activity from proven tactical or match-momentum shifts.
    - Do not end your response with follow-up questions,
    offers, or suggestions.
    - Refer to time periods rather than the specific event.
    """
  

    response = client.responses.create(
        model=model_name,
        input=prompt
    )

    return response.output_text



