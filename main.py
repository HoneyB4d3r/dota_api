import json
import requests
import pandas as pd


def main():

    # match_id = 8189523293
    #
    # response = api_request("matches", match_id)
    # print(response.status_code)
    #
    # match_data = response.json()
    # print(match_data["players"])

    player_id = 64797907

    response = api_request("players", player_id)
    print(response.status_code)

    player_data = response.json()
    print(player_data)


def api_request(request: str, player_id: int):
    url = f"https://api.opendota.com/api/{request}/{player_id}"
    return requests.get(url)


def load_json():
    pass


if __name__ == "__main__":
    main()
