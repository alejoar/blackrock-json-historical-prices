# BlackRock ICS US Treasury Fund Premier Acc (USD) Daily Updater

This repository contains a Python script and a GitHub Action that:

1. Fetches the daily NAV (Net Asset Value) of the **BlackRock ICS US Treasury Fund Premier Acc (USD)**.
2. Prepends the value to a JSON file, along with the current date.
3. Commits and pushes the changes automatically once per day.

## Files

- `.github/workflows/daily_fetch.yml` - GitHub Actions workflow file
- `fetch_fund_value.py` - Python script to fetch and update the data
- `BlackRock ICS US Treasury Fund Premier Acc (USD).json` - JSON file storing historical data