import requests
import json
import time
import os
from dotenv import load_dotenv
from testdbinit import insert_match_row, get_last_stored_matchweek
from jobs.logger import logger

load_dotenv('.env')
TOKEN = os.getenv("TOKEN")

curr_matchday = get_last_stored_matchweek()
logger.info(f"CURRENT MATCHDAY: {curr_matchday}")

# for matchday in range(curr_matchday, 39):
url = f"https://api.football-data.org/v4/competitions/PL/matches?matchday={curr_matchday}"    # matches on a certain matchday
headers = {"X-Auth-Token": TOKEN}

response = requests.get(url, headers=headers)
data = response.json()
# Pretty print
# print(json.dumps(data, indent=2))

with open(f'storage/matchday_{curr_matchday}_data.json', 'w') as f:
    f.write(json.dumps(data, indent=4))
matches_played = data["resultSet"]["played"]
matches_in_play = 0
matches_scheduled = 0
for m in data["matches"]:
    if m["status"] == "IN_PLAY":
        matches_in_play+=1
    if m["status"] == "TIMED":
        matches_scheduled+=1


if not matches_played:
    logger.info(f"matchday {curr_matchday} matches count is 0, breaking out of the loop")
else:
    logger.info(f"downloading matches from matchday {curr_matchday} (finished: {matches_played}, in play: {matches_in_play}, to be played: {matches_scheduled})")
    for match in data["matches"]:
        row = {}
        row["api_id"]               = match["id"]
        row["season"]               = data["filters"]["season"]
        row["matchday"]             = data["filters"]["matchday"]
        row["competition"]          = data["competition"]["code"]
        row["type"]                 = data["competition"]["type"]

        row["match_date"]           = match["utcDate"]
        row["status"]               = match["status"]
        row["home_team_full_name"]  = match["homeTeam"]["name"]
        row["home_team_short_name"] = match["homeTeam"]["shortName"]
        row["home_team_abbr"]       = match["homeTeam"]["tla"]
        row["home_team_crest"]      = match["homeTeam"]["crest"]

        row["away_team_full_name"]  = match["awayTeam"]["name"]
        row["away_team_short_name"] = match["awayTeam"]["shortName"]
        row["away_team_abbr"]       = match["awayTeam"]["tla"]
        row["away_team_crest"]      = match["awayTeam"]["crest"]

        row["home_team_ht_score"]   = match["score"]["halfTime"]["home"]
        row["home_team_ft_score"]   = match["score"]["fullTime"]["home"]
        row["away_team_ht_score"]   = match["score"]["halfTime"]["away"]
        row["away_team_ft_score"]   = match["score"]["fullTime"]["away"]
        row["winner"]               = match["score"]["winner"]
        row["referee"]              = match["referees"][0]["name"] if len(match["referees"]) else ""

        # print(json.dumps(row, indent=4))
        # print("----------------------------------------------")

        insert_match_row(row, "matches")
    


