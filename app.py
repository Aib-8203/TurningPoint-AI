
import streamlit as st
import pandas as pd

from src.events import load_match_events, get_events_in_window
from src.momentum import calculate_match_momentum
from src.momentum import detect_turning_points
from src.insight_agent import explain_turning_point



st.title("TurningPoint AI")

events = load_match_events("data/match_events_generated.json")

north_momentum = calculate_match_momentum(events, "North FC")
south_momentum = calculate_match_momentum(events, "South FC")


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

    turning_point = turning_points[0]
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







