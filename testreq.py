import requests
import json
import time
import os
from dotenv import load_dotenv
from testdbinit import insert_row

load_dotenv('.env')
TOKEN = os.getenv("TOKEN")

# url = "https://api.football-data.org/v4/competitions/PL/standings"  # current standings


for matchday in range(1, 38):
    url = f"https://api.football-data.org/v4/competitions/PL/matches?matchday={matchday}"    # matches on a certain matchday
    headers = {"X-Auth-Token": TOKEN}

    response = requests.get(url, headers=headers)
    data = response.json()

    # Pretty print
    # print(json.dumps(data, indent=2))

    with open(f'matchday_{matchday}_data.json', 'w') as f:
        f.write(json.dumps(data, indent=4))
    matches_played = data["resultSet"]["played"]
    # break

    if not matches_played:
        print(f"matchday {matchday} matches count is 0, breaking out of the loop")
        break

    print(f"downloading matches from matchday {matchday} ({matches_played})")

    for match in data["matches"]:
        row = {}
        row["api_id"] = match["id"]
        row["season"] = data["filters"]["season"]
        row["matchday"] = data["filters"]["matchday"]
        row["competition"] = data["competition"]["code"]
        row["type"] = data["competition"]["type"]

        row["match_date"] = match["utcDate"]
        row["status"] = match["status"]
        row["home_team_full_name"] = match["homeTeam"]["name"]
        row["home_team_short_name"] = match["homeTeam"]["shortName"]
        row["home_team_abbr"] = match["homeTeam"]["tla"]
        row["home_team_crest"] = match["homeTeam"]["crest"]

        row["away_team_full_name"] = match["awayTeam"]["name"]
        row["away_team_short_name"] = match["awayTeam"]["shortName"]
        row["away_team_abbr"] = match["awayTeam"]["tla"]
        row["away_team_crest"] = match["awayTeam"]["crest"]

        row["home_team_ht_score"] = match["score"]["halfTime"]["home"]
        row["home_team_ft_score"] = match["score"]["fullTime"]["home"]
        row["away_team_ht_score"] = match["score"]["halfTime"]["away"]
        row["away_team_ft_score"] = match["score"]["fullTime"]["away"]
        row["winner"] = match["score"]["winner"]
        row["referee"] = match["referees"][0]["name"]

        # print(json.dumps(row, indent=4))
        # print("----------------------------------------------")

        insert_row(row)
        
    print("sleeping 7s...") # free plan supports up to 10 calls/min
    time.sleep(7)


