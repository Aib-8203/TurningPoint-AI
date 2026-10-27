
import random
import json

rng = random.Random(42)

events = []

for event_id in range(1, 121):
    minute = rng.randint(0, 89)
    
    if minute < 30:
     weights = [50, 50]

    elif minute < 60:
     weights = [25, 75]

    else:
     weights = [75, 25]

    team = rng.choices(
    ["North FC", "South FC"],
    weights=weights,
    k=1
 )[0]

    event_types = ["pass", "recovery", "shot", "foul"]
    event_weights = [55, 25, 15, 5]
    event_type = rng.choices(event_types, weights= event_weights,k=1)[0]


    if event_type == "shot":
     outcome = rng.choice(
        ["saved", "goal", "missed", "blocked"]
    )
    elif event_type == "pass":
     outcome = rng.choice(["successful","unsuccessful"])

    elif event_type == "recovery":
     outcome = "successful"
    

    else:
     outcome = rng.choice(["committed"])


    event = {
    "event_id": event_id,
    "minute": minute,
    "team": team,
    "type": event_type,
    "outcome": outcome

}
    events.append(event)

events.sort(key=lambda event: event["minute"])

with open("data/match_events_generated.json", "w") as file:
    json.dump(events, file, indent=4)










        


