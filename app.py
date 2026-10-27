
import streamlit as st
import pandas as pd

from src.events import load_match_events, get_events_in_window
from src.momentum import calculate_match_momentum
from src.momentum import detect_turning_points
from src.insight_agent import explain_turning_point



st.title("TurningPoint AI")

events = load_match_events("data/match_events.json")

north_momentum = calculate_match_momentum(events, "North FC")
south_momentum = calculate_match_momentum(events, "South FC")


north_df = pd.DataFrame(north_momentum)
south_df = pd.DataFrame(south_momentum)

comparison_df = pd.merge(north_df, south_df, on="minute")

st.subheader("Weighted attacking activity score")

st.line_chart(
    comparison_df,
    x="minute",
    y=["North FC", "South FC"], 
    
)


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


north_turning_points = detect_turning_points(
    north_momentum, threshold=5
)

south_turning_points = detect_turning_points(
    south_momentum, threshold=5
)


selected_team = st.selectbox(
    "Select team to analyse",
    ["North FC", "South FC"]
)

if selected_team == "North FC":
    turning_points = north_turning_points
else:
    turning_points = south_turning_points


audience = st.radio(
    "choose viewing mode",
    ["Casual Fan", "Analyst"]
)


if st.button("Generate AI Insight"):

    received_info = explain_turning_point(turning_point, previous_events, current_events, audience)

    st.write(received_info)


with st.expander("View supporting match evidence"):

    st.write("Selected turning point:")
    st.json(turning_point)

    st.write("Previous events:")
    if previous_events:
        st.dataframe(previous_events)
    else:
        st.info("No recorded events in the previous period.")

    st.write("Current events:")
    st.dataframe(current_events)


selected_team = st.selectbox(
    "Select team to analyse",
    ["North FC", "South FC"]
)

if selected_team == "North FC":
    turning_points = north_turning_points
else:
    turning_points = south_turning_points





