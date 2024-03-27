import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Fetch data from the Sleeper API
url = "https://api.sleeper.app/v1/players/nfl"
response = requests.get(url)
players_data = response.json()

# Process the fetched data
qb_data = []
wr_data = []
rb_data = []
te_data = []

for player_id, player_info in players_data.items():
    if "fantasy_positions" in player_info:
        if "QB" in player_info["fantasy_positions"]:
            qb_data.append({"name": player_info["first_name"] + " " + player_info["last_name"], "player_id": player_id})
        if "WR" in player_info["fantasy_positions"]:
            wr_data.append({"name": player_info["first_name"] + " " + player_info["last_name"], "player_id": player_id})
        if "RB" in player_info["fantasy_positions"]:
            rb_data.append({"name": player_info["first_name"] + " " + player_info["last_name"], "player_id": player_id})
        if "TE" in player_info["fantasy_positions"]:
            te_data.append({"name": player_info["first_name"] + " " + player_info["last_name"], "player_id": player_id})

qb_df = pd.DataFrame(qb_data)
wr_df = pd.DataFrame(wr_data)
rb_df = pd.DataFrame(rb_data)
te_df = pd.DataFrame(te_data)

# Fetch trending players data
def get_trending_players(position):
    url = f"https://api.sleeper.app/v1/players/nfl/trending/add?lookback_hours=24&limit=25"
    response = requests.get(url)
    trending_players = response.json()

    trending_data = []
    for player in trending_players:
        if player["player_id"] in players_data:
            player_info = players_data[player["player_id"]]
            if position in player_info["fantasy_positions"]:
                trending_data.append({"name": player_info["first_name"] + " " + player_info["last_name"], "count": player["count"]})

    return pd.DataFrame(trending_data)

qb_trending_df = get_trending_players("QB")
wr_trending_df = get_trending_players("WR")
rb_trending_df = get_trending_players("RB")
te_trending_df = get_trending_players("TE")

# Create interactive charts using Plotly
def create_trending_chart(df, position):
    if not df.empty:
        fig = px.bar(df, x="name", y="count", title=f"Trending {position}s (Last 24 hours)")
        fig.update_layout(xaxis_title="Player", yaxis_title="Number of Adds")
        return fig
    else:
        return None

qb_trending_chart = create_trending_chart(qb_trending_df, "QB")
wr_trending_chart = create_trending_chart(wr_trending_df, "WR")
rb_trending_chart = create_trending_chart(rb_trending_df, "RB")
te_trending_chart = create_trending_chart(te_trending_df, "TE")

# Build the Streamlit app
st.set_page_config(page_title="Fantasy Football Insights", layout="wide")

st.title("Fantasy Football Insights")

st.header("Trending Players (Last 24 hours)")

col1, col2 = st.columns(2)

with col1:
    if qb_trending_chart:
        st.subheader("Quarterbacks")
        st.plotly_chart(qb_trending_chart)
    
    if rb_trending_chart:
        st.subheader("Running Backs")
        st.plotly_chart(rb_trending_chart)

with col2:
    if wr_trending_chart:
        st.subheader("Wide Receivers")
        st.plotly_chart(wr_trending_chart)
    
    if te_trending_chart:
        st.subheader("Tight Ends")
        st.plotly_chart(te_trending_chart)

# Additional insights and features
st.header("Player Lookup")

selected_position = st.selectbox("Select Position", ["QB", "WR", "RB", "TE"])

if selected_position == "QB":
    selected_player = st.selectbox("Select Player", qb_df["name"])
    player_id = qb_df[qb_df["name"] == selected_player]["player_id"].values[0]
elif selected_position == "WR":
    selected_player = st.selectbox("Select Player", wr_df["name"])
    player_id = wr_df[wr_df["name"] == selected_player]["player_id"].values[0]
elif selected_position == "RB":
    selected_player = st.selectbox("Select Player", rb_df["name"])
    player_id = rb_df[rb_df["name"] == selected_player]["player_id"].values[0]
else:
    selected_player = st.selectbox("Select Player", te_df["name"])
    player_id = te_df[te_df["name"] == selected_player]["player_id"].values[0]

player_info = players_data[player_id]
st.subheader("Player Information")
st.write(f"Name: {player_info['first_name']} {player_info['last_name']}")
st.write(f"Position: {', '.join(player_info['fantasy_positions'])}")
st.write(f"Team: {player_info['team']}")
st.write(f"Status: {player_info['status']}")