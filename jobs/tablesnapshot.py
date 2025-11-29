import sqlite3
import json
from app.dbinit import insert_row_snapshot, db_conn
from app.utils.logger import logger
import hashlib

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

# print(standings)

table = sorted(
    standings.items(),
    key=lambda x: (x[1]["points"], x[1]["goals_for"] - x[1]["goals_against"]),
    reverse=True
)
serialized_table = json.dumps(table, indent=4)

table_hash = hashlib.sha256(serialized_table.encode("utf-8")).hexdigest()
print(table_hash)

print(json.dumps(table, indent=4))
cursor.execute("SELECT COALESCE(MAX(snapshot_id), 0) FROM table_snapshots")
snapshot_id = cursor.fetchone()[0]
next_snapshot_id = snapshot_id + 1
print(snapshot_id)

# fetch latest table
last_table_sql = f"SELECT * FROM table_snapshots WHERE snapshot_id={snapshot_id}"
print(last_table_sql)
cursor.execute(last_table_sql)
last_inserted_table = [dict(row) for row in cursor.fetchall()]

print(last_inserted_table)
print(json.dumps(last_inserted_table, indent=4))
# repack the data to fit the dict above that we are going to compare it to

# make hash out of it

# comapare it to the one we want to insert

# insert if they are different


logger.info(f"Making snapshot with id {next_snapshot_id}")
for idx, item in enumerate(table, start=1):
    data = {}
    goal_diff = item[1]["goals_for"] - item[1]["goals_against"]
    item[1]["goal_difference"] = goal_diff
    data = item[1]
    data['team_name'] = item[0]
    data["type"] = 'regular'
    data["snapshot_id"] = next_snapshot_id
    insert_row_snapshot(data, "table_snapshots")
    # print(data)
    
conn.close()
