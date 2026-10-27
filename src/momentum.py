
EVENT_WEIGHTS = {
    "shot": 5,
    "recovery": 3,
    "pass": 1,
    "foul": 0
}
def calculate_momentum(events, team, start_minute, end_minute):
    score = 0

    for event in events:
        if event["team"] == team and start_minute <= event["minute"] <= end_minute:
            event_type = event["type"]
            weight = EVENT_WEIGHTS.get(event_type, 0)
            score += weight
    return score



def calculate_match_momentum(events, team):
    momentum_data = []

    for start_minute in range(0,90,10):
        end_minute = start_minute + 9

        current_period = calculate_momentum(events, team, start_minute,end_minute)

        current_result = {"minute" : start_minute, "score": current_period}

        momentum_data.append(current_result)

    return momentum_data


def detect_turning_points(momentum_data, threshold=5):
    turning_points = []

    for i in range(1,len(momentum_data)):

     current_score = momentum_data[i]["score"]
     previous_score = momentum_data[i-1]["score"]
     score_difference = current_score - previous_score

     if score_difference >= threshold:
      turning_points.append({
      "minute": momentum_data[i]["minute"],
      "score": current_score,
      "previous_score": previous_score,
      "change": score_difference
})

     

    return turning_points

