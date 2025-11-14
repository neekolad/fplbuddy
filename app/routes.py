from flask import Blueprint, render_template
from .models import get_db_connection

main = Blueprint("main", __name__)

@main.route("/")
def index():
    conn = get_db_connection()
    # Fetch latest snapshot ID
    snapshot_id = conn.execute("SELECT MAX(snapshot_id) as max_id FROM table_snapshots").fetchone()["max_id"]

    # Fetch rows for that snapshot (you can also filter by type if you have that column)
    rows = conn.execute(
        "SELECT * FROM table_snapshots WHERE snapshot_id = ? ORDER BY points DESC, goals_for - goals_against DESC, goals_for DESC",
        (snapshot_id,)
    ).fetchall()

    conn.close()
    return render_template("index.html", title="Premier League Table", rows=rows)
