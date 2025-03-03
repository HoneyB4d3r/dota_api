import argparse
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

from datetime import datetime, timezone


def main():
    st.set_page_config(
        page_title="DotA 2 Player Stats",
        page_icon=":video_game:",
    )
    args = arg_handler()

    response_matches = api_request("players", args.ID, "matches")
    df_matches = pd.DataFrame(response_matches.json())
    df_matches = convert_unix_time(df_matches, "start_time")
    df_matches.set_index("match_id", inplace=True)

    response_pros = api_request("players", args.ID, "pros")
    df_pros = pd.DataFrame(response_pros.json())
    df_pros = convert_unix_time(df_pros, "last_played")

    build_dashboard(
        df_matches,
        df_pros[
            [
                "name",
                "team_name",
                "last_played",
                "win",
                "games",
                "with_win",
                "with_games",
                "against_win",
                "against_games",
            ]
        ],
    )
    print(response_matches.status_code)
    print(response_pros.status_code)


def build_dashboard(df_matches, df_pros):
    st.title("Player Stats")
    st.dataframe(df_matches)
    build_kda(df_matches)
    build_pychart(df_matches["radiant_win"])
    st.title("Player's matches with pros")
    st.dataframe(df_pros)
    get_last_pro_matches(df_matches, df_pros)


@st.cache_data(ttl=3600)
def get_last_pro_matches(df_matches, df_pros):
    for _, row in df_pros.iterrows():
        pro_match = df_matches.loc[
            df_matches["start_time"] == row["last_played"]
        ]
        st.write(row["name"], row["win"], row["with_win"], pro_match)


@st.cache_data(ttl=3600)
def build_pychart(data):
    radiant_win = data.describe()["freq"]
    dire_win = data.describe()["count"] - radiant_win
    fig, ax = plt.subplots(figsize=(2, 2))
    fig.set_facecolor("#00000000")
    ax.pie(
        [radiant_win, dire_win],
        labels=["Radiant", "Dire"],
        autopct="%1.1f%%",
        colors=["#3333ff", "#ff0000"],
        textprops={
            "color": "#ffffff",
            "fontsize": 6,
        },
        shadow=True,
    )
    st.write("Win Distribution")
    st.pyplot(fig, use_container_width=False)


@st.cache_data(ttl=3600)
def build_kda(data):
    st.write("KDA-chart")
    st.line_chart(
        data[["start_time", "kills", "assists", "deaths"]].head(50),
        x="start_time",
        y=["kills", "assists", "deaths"],
        x_label="Time",
        color=["#ffcc00", "#ff0000", "#3333ff"],
    )


@st.cache_data(ttl=3600)
def convert_unix_time(data, *columns: str):
    for index, row in data.iterrows():
        for column in columns:
            utc_time = datetime.fromtimestamp(
                row[column], tz=timezone.utc
            ).strftime(r"%Y-%m-%d %H:%M:%S")
            data.at[index, column] = utc_time
    return data


def arg_handler():
    parser = argparse.ArgumentParser(
        prog="DotA data analysis", description="Analysis of DotA-player data"
    )
    parser.add_argument("--ID", default=None, help="Player ID", type=int)
    return parser.parse_args()


@st.cache_data(ttl=3600, show_spinner="Fetching data from API...")
def api_request(request: str, player_id: int, *paths: str):
    url = f"https://api.opendota.com/api/{request}/{player_id}"
    for path in paths:
        url += f"/{path}"
    return requests.get(url)


def load_json():
    pass


if __name__ == "__main__":
    main()
