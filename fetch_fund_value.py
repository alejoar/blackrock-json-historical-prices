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
    Prepends or replaces the data for today's date in the JSON file.
    - If the latest entry already has today's date, replace it.
    - Otherwise, add a new entry at the top of the array.
    """
    # 1. Read the existing JSON
    try:
        with open(JSON_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty/corrupt, start with an empty list
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

    # 3. Check if the most recent entry in data already has today's date
    if data and data[0].get("date") == today_str:
        # Replace the existing record for today
        print(f"Found an existing record for {today_str}, replacing it with new data.")
        data[0] = new_record
    else:
        # Prepend the new record if today's date doesn't exist
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
