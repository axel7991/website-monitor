import streamlit as st
import plotly.express as px
import pandas as pd
import json
import os

st.set_page_config(page_title="Website Monitor", page_icon="🔍", layout="wide")

st.title("🔍 Website Change Monitor")
st.markdown("Track changes across your monitored websites in real time.")

if not os.path.exists("change_history.json"):
    st.warning("No change history yet. Run monitor.py first.")
else:
    with open("change_history.json", "r") as f:
        history = json.load(f)

    df = pd.DataFrame(history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["total_changes"] = df["lines_added"] + df["lines_removed"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Checks", len(df))
    col2.metric("Total Changes Detected", len(df[df["total_changes"] > 0]))
    col3.metric("URLs Monitored", df["url"].nunique())

    st.subheader("📈 Changes Over Time")
    fig = px.line(df, x="timestamp", y="total_changes",
                  title="Website Changes Over Time",
                  labels={"total_changes": "Lines Changed", "timestamp": "Time"},
                  markers=True)
    fig.update_traces(line_color="#6366f1")
    st.plotly_chart(fig, use_container_width=True)

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("➕ Lines Added vs ➖ Removed")
        fig2 = px.bar(df, x="timestamp", y=["lines_added", "lines_removed"],
                      barmode="group",
                      labels={"value": "Lines", "timestamp": "Time"})
        st.plotly_chart(fig2, use_container_width=True)

    with col5:
        st.subheader("📋 Change History")
        st.dataframe(df[["timestamp", "url", "lines_added", "lines_removed"]]
                     .sort_values("timestamp", ascending=False),
                     use_container_width=True)