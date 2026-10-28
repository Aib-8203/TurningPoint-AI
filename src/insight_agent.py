
import os
import json
from openai import OpenAI

def explain_turning_point(turning_point, previous_events, current_events, audience):

    model_name = os.environ["FOUNDRY_MODEL_NAME"]

    
    client = OpenAI(
    base_url=os.environ["FOUNDRY_INFERENCE_BASE_URL"],
    api_key=os.environ["FOUNDRY_API_KEY"]
)


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

    
    IMPORTANT OUTPUT RULES:
    - The selected audience is: {audience}.
    - Generate exactly ONE explanation for this audience.
    - Do NOT generate an explanation for the other audience.
    - Do NOT include headings such as "Analyst mode"
      or "Casual Fan mode".
    - If Casual Fan is selected, use only simple,
      engaging football language in two sentences.
    - If Analyst is selected, provide technical
      analysis with supporting event IDs and limitations.
    - Return only the explanation, nothing else.

    """
  

    response = client.responses.create(
        model=model_name,
        input=prompt
    )

    return response.output_text



