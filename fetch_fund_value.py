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

    # data_element might look like: "USD 118.5825"
    text_value = data_element.get_text(strip=True)  # e.g. "USD 118.5825"

    # Remove "USD " from the text and convert to float
    _, value_str = text_value.split()
    return float(value_str)


def update_json_file(new_value):
    """
    Prepends a new entry with today's date and the new_value
    to the JSON file JSON_FILE.
    """
    # 1. Read the existing JSON
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file not found or empty/corrupt, start with an empty list
        data = []

    # 2. Create a new record
    today_str = datetime.utcnow().strftime("%Y-%m-%d")

    new_record = {
        "date": today_str,
        "open": new_value,
        "high": new_value,
        "low": new_value,
        "close": new_value,
        "adjusted_close": new_value,
        "volume": None,
    }

    # 3. Prepend the new record to the existing data
    data.insert(0, new_record)

    # 4. Save the updated data back to the file
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)


def main():
    # Fetch the fund value
    fund_value = fetch_fund_value()

    # Update the JSON file
    update_json_file(fund_value)


if __name__ == "__main__":
    main()
