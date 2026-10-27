import json

def load_match_events(filename):
    with open(filename, 'r') as file:
        match_events = json.load(file)
    return match_events


def get_events_in_window(events, team, start_minute, end_minute):
    matching_events = []

    for event in events:
        if event["team"] == team  and start_minute <= event["minute"] <= end_minute:
            matching_events.append(event)
    return matching_events

    

