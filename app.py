
import streamlit as st
import pandas as pd

from src.events import load_match_events, get_events_in_window
from src.momentum import calculate_match_momentum
from src.momentum import detect_turning_points
from src.insight_agent import explain_turning_point



st.title("TurningPoint AI")


all_events = load_match_events(
    "data/match_events_generated.json"
)

replay_minute = st.slider(
    "Replay match through minute",
    min_value=9,
    max_value=89,
    value=89,
    step=10
)

events = [
    event for event in all_events
    if event["minute"] <= replay_minute
]


north_momentum = calculate_match_momentum(events, "North FC")
south_momentum = calculate_match_momentum(events, "South FC")


north_momentum = [
    row for row in north_momentum
    if row["minute"] + 9 <= replay_minute
]

south_momentum = [
    row for row in south_momentum
    if row["minute"] + 9 <= replay_minute
]



north_df = pd.DataFrame(north_momentum)
south_df = pd.DataFrame(south_momentum)

comparison_df = pd.merge(north_df, south_df, on="minute")

st.subheader("Weighted attacking activity score")


comparison_df = comparison_df.rename(
    columns={
        "score_x": "North FC",
        "score_y": "South FC"
    }
    
)

st.line_chart(
    comparison_df,
    x="minute",
    y=["North FC", "South FC"], 

)

selected_team = st.selectbox(
    "Select team to analyse",
    ["North FC", "South FC"]
)

if selected_team == "North FC":
    selected_momentum = north_momentum
else:
    selected_momentum = south_momentum

turning_points = detect_turning_points(
    selected_momentum,
    threshold=5
)


st.subheader(f"Detected Turning Points — {selected_team}")


if turning_points:
    st.dataframe(turning_points)

    selected_index = st.selectbox(
        "Select a turning point",
        options=range(len(turning_points)),
        format_func=lambda i: (
            f"Minute {turning_points[i]['minute']} "
            f"— +{turning_points[i]['change']} activity"
        ),
        key=f"turning_point_{selected_team}"
    )

    turning_point = turning_points[selected_index]
    current_start = turning_point["minute"]


    previous_events = get_events_in_window(events, selected_team, current_start - 10, current_start - 1)
    current_events = get_events_in_window(events, selected_team, current_start , current_start + 9)


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



    audience = st.radio(
    "choose viewing mode",
    ["Casual Fan", "Analyst"]
)


    if st.button("Generate AI Insight"):

     received_info = explain_turning_point(turning_point, previous_events, current_events, audience)

     st.write(received_info)

else:
    st.info("No significant attacking shifts detected.")







