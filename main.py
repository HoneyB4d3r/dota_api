import argparse
import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

from datetime import datetime, timezone


def main():
    args = arg_handler()

    response = api_request("players", args.ID, "matches")
    print(response.status_code)
    df = pd.DataFrame(response.json())
    df = convert_unix_time(df)
    df.set_index("match_id", inplace=True)
    build_dashboard(df)

    response = api_request("players", args.ID, "pros")
    st.dataframe(pd.DataFrame(response.json()))


def build_dashboard(data):
    build_kda(data)
    st.write("Win Distribution")
    build_pychart(data["radiant_win"])


@st.cache_data(ttl=3600)
def build_pychart(data):
    radiant_win = data.describe()["freq"]
    dire_win = data.describe()["count"] - radiant_win
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.set_facecolor("#00000000")
    ax.pie(
        [radiant_win, dire_win],
        labels=["Radiant", "Dire"],
        autopct="%1.1f%%",
        colors=["#3333ff", "#ff0000"],
        textprops={"color": "#ffffff"},
    )
    st.pyplot(fig)


@st.cache_data(ttl=3600)
def build_kda(data):
    st.title("DotA 2 Player Statistics")
    st.dataframe(data)
    st.line_chart(
        data[["start_time", "kills", "assists", "deaths"]].head(50),
        x="start_time",
        y=["kills", "assists", "deaths"],
        x_label="Time",
        color=["#ffcc00", "#ff0000", "#3333ff"],
    )


@st.cache_data(ttl=3600)
def convert_unix_time(data):
    for index, row in data.iterrows():
        utc_time = datetime.fromtimestamp(
            row["start_time"], tz=timezone.utc
        ).strftime(r"%Y-%m-%d %H:%M:%S")
        data.at[index, "start_time"] = utc_time
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
