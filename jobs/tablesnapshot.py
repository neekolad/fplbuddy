import sqlite3
import json
from app.dbinit import insert_row_snapshot, db_conn
from app.utils.logger import logger
import hashlib


def repack_table(data):
    '''repack data fetched from db to match data we are comaparing it to'''
    repacked_data = {}
    for item in data:
        repacked_data[item["team_name"]] = {
                "played" : item["played"],
                "wins" : item["wins"],
                "draws" : item["draws"],
                "losses" : item["losses"],
                "goals_for" : item["goals_for"],
                "goals_against" : item["goals_against"],
                "points" : item["points"]
            }
    table = sorted(
        repacked_data.items(),
        key=lambda x: (x[1]["points"], x[1]["goals_for"] - x[1]["goals_against"]),
        reverse=True
    )
    serialized_table = json.dumps(table, indent=4)
    print("OLD TABLE:", serialized_table)
    return serialized_table
        
def is_different_table(old_table, new_table):
    '''compare 2 tables'''
    if old_table == new_table:
        return False
    return True


conn = db_conn()
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
res = cursor.execute("SELECT * FROM matches WHERE `competition`='PL' AND `status`='FINISHED'")
standings = {}

for match in res.fetchall():
    home = match["home_team_full_name"]
    away = match["away_team_full_name"]
    home_score = match["home_team_ft_score"]
    away_score = match["away_team_ft_score"]

    # Ensure teams exist in dict
    for team in [home, away]:
        if team not in standings:
            standings[team] = {
                "played": 0, "wins": 0, "draws": 0, "losses": 0,
                "goals_for": 0, "goals_against": 0, "points": 0
            }

    standings[home]["played"] += 1
    standings[away]["played"] += 1

    standings[home]["goals_for"] += home_score
    standings[home]["goals_against"] += away_score
    standings[away]["goals_for"] += away_score
    standings[away]["goals_against"] += home_score

    if home_score > away_score:
        standings[home]["wins"] += 1
        standings[away]["losses"] += 1
        standings[home]["points"] += 3
    elif away_score > home_score:
        standings[away]["wins"] += 1
        standings[home]["losses"] += 1
        standings[away]["points"] += 3
    else:
        standings[home]["draws"] += 1
        standings[away]["draws"] += 1
        standings[home]["points"] += 1
        standings[away]["points"] += 1

print(standings)

new_table = sorted(
    standings.items(),
    key=lambda x: (x[1]["points"], x[1]["goals_for"] - x[1]["goals_against"]),
    reverse=True
)
serialized_new_table = json.dumps(new_table, indent=4)
# print("NEW TABLE:", serialized_new_table)

new_table_hash = hashlib.sha256(serialized_new_table.encode("utf-8")).hexdigest()
# print("NEW TABLE HASH:", new_table_hash)

# print(json.dumps(table, indent=4))
cursor.execute("SELECT COALESCE(MAX(snapshot_id), 0) FROM table_snapshots")
snapshot_id = cursor.fetchone()[0]
next_snapshot_id = snapshot_id + 1
# print(snapshot_id)

# fetch latest table
last_table_sql = f"SELECT * FROM table_snapshots WHERE snapshot_id={snapshot_id}"
cursor.execute(last_table_sql)
last_inserted_table = [dict(row) for row in cursor.fetchall()]
# print(last_inserted_table)
# print(json.dumps(last_inserted_table, indent=4))

# repack the data to fit the dict above that we are going to compare it to
repacked_last_table = repack_table(last_inserted_table)

# make hash out of it
repacked_table_hash = hashlib.sha256(repacked_last_table.encode("utf-8")).hexdigest()
print("OLD TABLE HASH:", repacked_table_hash)

# comapare it to the one we want to insert
if is_different_table(new_table_hash, repacked_table_hash):
    # insert new updated table if they are different
    logger.info(f"Making snapshot with id {next_snapshot_id}")
    for idx, item in enumerate(new_table, start=1):
        data = {}
        goal_diff = item[1]["goals_for"] - item[1]["goals_against"]
        item[1]["goal_difference"] = goal_diff
        data = item[1]
        data['team_name'] = item[0]
        data["type"] = 'regular'
        data["snapshot_id"] = next_snapshot_id
        insert_row_snapshot(data, "table_snapshots")
        # print(data)
else:
    print("Not inserting new table because its the same as the old one")


conn.close()
