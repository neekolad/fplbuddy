#TODO:

- refactor code
- */1 * * * * /home/nikola/projects/fplbuddy/venv/bin/python3 /home/nikola/projects/fplbuddy/app/jobs/fetch_matches.py >> logs/$(date +\%Y\%m).log 2>&1 &