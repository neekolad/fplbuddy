#TODO:

- refactor code
- cron */5 * * * * cd /home/youruser/project && /usr/bin/python3 jobs/fetch_matches.py >> logs/$(date +\%Y\%m).log 2>&1
