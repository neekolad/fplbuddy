#TODO:

- refactor code
- fetch matches cron */15 * * * * cd /home/nikola/projects/fplbuddy && /home/nikola/projects/fplbuddy/venv/bin/python3 -m jobs.fetch_matches >> logs/fetch_$(date +\%Y\%m).log 2>&1 &
- make snapshot cron */9 * * * * cd /home/nikola/projects/fplbuddy && /home/nikola/projects/fplbuddy/venv/bin/python3 -m jobs.tablesnapshot >> logs/snapshot_$(date +\%Y\%m).log 2>&1 &