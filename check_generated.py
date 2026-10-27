from src.events import load_match_events
from src.momentum import calculate_match_momentum, detect_turning_points

print("TEST SCRIPT IS RUNNING")

events = load_match_events("data/match_events_generated.json")

print("Total events:", len(events))

for team in ["North FC", "South FC"]:
    momentum = calculate_match_momentum(events, team)
    turning_points = detect_turning_points(momentum, threshold=5)

    print(f"\n{team}")
    print("Momentum:", momentum)
    print("Turning points:", turning_points)