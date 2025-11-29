#TODO:

- refactor code
- fetch matches cron */15 * * * * cd /home/nikola/projects/fplbuddy && /home/nikola/projects/fplbuddy/venv/bin/python3 -m jobs.fetch_matches >> logs/fetch_$(date +\%Y\%m).log 2>&1 &
- make snapshot cron */9 * * * * cd /home/nikola/projects/fplbuddy && /home/nikola/projects/fplbuddy/venv/bin/python3 -m jobs.tablesnapshot >> logs/snapshot_$(date +\%Y\%m).log 2>&1 &
- make snapshot table which will take last snapshot sort it and make hash out of it, compare it to the new snapshot, if the snapshots are different insert new snapshot (this table will be used for historical changes not only by matchweek but by change!)
- make LIVE TABLE which will have unique api id key and use insert or update, and make frontend use this table for quick live view