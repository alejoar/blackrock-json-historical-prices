#!/usr/bin/env python3
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = "https://www.blackrock.com/cash/en-es/products/250972/blackrock-ics-us-treasury-premier-acc-fund/"
JSON_FILE = "BlackRock ICS US Treasury Fund Premier Acc (USD).json"


def fetch_fund_value():
    """
    Fetches the fund value from the given BlackRock ICS US Treasury Fund page.
    The element of interest has the class: '.header-nav-data'
    Returns a float value, e.g. 118.5825
    """
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    data_element = soup.select_one(".header-nav-data")

    # Example text_value: "USD 118.5825"
    text_value = data_element.get_text(strip=True)

    # Remove "USD " from the text and convert to float
    _, value_str = text_value.split()
    return float(value_str)


def update_json_file(new_value):
    """
    - If the most recent entry (data[0]) has the same 'close' value as new_value, do nothing.
    - Otherwise:
      - If the latest entry is today's date:
         - Replace if the value is different.
      - Else, prepend a new entry.
    """
    # 1. Read the existing JSON
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty/corrupt, start with an empty list
        data = []

    # 2. Check if the most recent (top) entry has the same value
    if data:
        latest_value = data[0].get("close")  # 'close', 'open', etc. are the same
        if latest_value == new_value:
            # The value is exactly the same as the last entry => do nothing
            print(
                f"The last read value ({latest_value}) is the same as the new value ({new_value}). Skipping update."
            )
            return

    # 3. Prepare today's record
    today_str = datetime.utcnow().strftime("%Y-%m-%d")

    # Helper to create a new record dict
    def create_record(date_str, value):
        return {
            "date": date_str,
            "open": value,
            "high": value,
            "low": value,
            "close": value,
            "adjusted_close": value,
            "volume": None,
        }

    new_record = create_record(today_str, new_value)

    # 4. Check if the top entry is today's date
    if data and data[0].get("date") == today_str:
        # If top entry is today's date, replace it with the new value
        print(f"Updating record for {today_str} with new value {new_value}.")
        data[0] = new_record
    else:
        # Otherwise, prepend a new record
        print(f"Prepending a new record for {today_str} with value {new_value}.")
        data.insert(0, new_record)

    # 5. Save the updated data back to the file
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():
    # Fetch the fund value
    fund_value = fetch_fund_value()

    # Update the JSON file
    update_json_file(fund_value)


if __name__ == "__main__":
    main()
