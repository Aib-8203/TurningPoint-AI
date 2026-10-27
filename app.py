
import streamlit as st
import pandas as pd

from src.events import load_match_events, get_events_in_window
from src.momentum import calculate_match_momentum
from src.momentum import detect_turning_points
from src.insight_agent import explain_turning_point



st.title("TurningPoint AI")

events = load_match_events("data/match_events.json")

north_momentum = calculate_match_momentum(
    events, "North FC"
)

df = pd.DataFrame(north_momentum)

st.subheader("North FC Attacking Momentum")
st.dataframe(df)
st.line_chart(df, x="minute", y="score")


turning_points = detect_turning_points(
    north_momentum, threshold=5
)

st.subheader("Detected Turning Points")

if turning_points:
    st.dataframe(turning_points)
else:
    st.info("No significant attacking shifts detected.")

if turning_points:
    turning_point = turning_points[0]
    current_start = turning_point["minute"]

previous_events = get_events_in_window(events, "North FC", current_start - 10, current_start - 1)
current_events = get_events_in_window(events, "North FC", current_start , current_start + 9)

st.write("Selected turning point:", turning_point)
st.write("Previous events:", previous_events)
st.write("Current events:", current_events)

audience = st.radio(
    "choose viewing mode",
    ["Casual Fan", "Analyst"]
)


if st.button("Generate AI Insight"):

    received_info = explain_turning_point(turning_point, previous_events, current_events, audience)

    st.write(received_info)




