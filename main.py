import argparse
import json
import pandas as pd
import requests
import streamlit as st

from datetime import datetime, timezone


def main():
    args = arg_handler()
    print(args)
    if player_id := args.load:
        df = convert_unix_time(load_data(player_id))
        build_dashboard(df)
    elif player_id := args.request:
        response = api_request("players", player_id, "matches")
        print(response.status_code)
        player_data = response.json()
        save_data(player_data, player_id)


def build_dashboard(data):
    st.title("DotA 2 Player Statistics")
    st.dataframe(data)


@st.cache_data(ttl=3600)
def convert_unix_time(data):
    for index, row in data.iterrows():
        utc_time = datetime.fromtimestamp(
            row["start_time"], tz=timezone.utc
        ).strftime(r"%Y-%m-%d %H:%M:%S")
        data.at[index, "start_time"] = utc_time
    return data


@st.cache_data(ttl=3600, show_spinner="Loading data...")
def load_data(file_name: str):
    df = pd.read_csv(f"{file_name}.csv")
    df.set_index("match_id", inplace=True)
    return df


def save_data(data, file_name: str):
    df = pd.DataFrame(data)
    df.set_index("match_id", inplace=True)
    df.to_csv(f"{file_name}.csv")


def arg_handler():
    parser = argparse.ArgumentParser(
        prog="DotA data analysis", description="Analydsis of DotA-player data"
    )
    parser.add_argument(
        "--load", default=None, help="User ID to load .csv-file", type=int
    )
    parser.add_argument(
        "--request", default=None, help="User ID to send request", type=int
    )
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

    # match_id = 8189523293
    #
    # response = api_request("matches", match_id)
    # print(response.status_code)
    #
    # match_data = response.json()
    # print(match_data["players"])
