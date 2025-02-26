import argparse
import json
import requests
import pandas as pd


def main():
    args = arg_handler()
    if player_id := args.load:
        df = pd.read_csv(f"{player_id}.csv")
        df.set_index("match_id", inplace=True)
        print(df)
    elif player_id := args.request:
        response = api_request("players", player_id, "matches")
        print(response.status_code)

        player_data = response.json()
        df = pd.DataFrame(player_data)
        df.set_index("match_id", inplace=True)
        df.to_csv(f"{player_id}.csv")


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
