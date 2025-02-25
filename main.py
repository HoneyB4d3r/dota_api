import json
import requests
import pandas as pd


def main():
    # match_id = "8189523293"
    # url = f"https://api.opendota.com/api/matches/{match_id}"
    player_id = "64797907"
    url = f"https://api.opendota.com/api/matches/{player_id}"
    response = requests.get(url)
    print(response.status_code)
    # match_data = response.json()
    player_data = response.json()
    print(player_data["profile"]["leaderboard_rank"])


if __name__ == "__main__":
    main()
