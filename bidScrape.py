import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

# Constants
URL = "https://www.bidspotter.com/en-gb/auction-catalogues/bscrma/catalogue-id-r-m-au10135/lot-8814c403-1603-4d65-b83d-b2190164952a"
CSV_FILE = "fanuc_bids.csv"
WAIT_TIME = 60  # Time to wait between checks in seconds

# Initialize CSV file with headers if it doesn't exist
try:
    with open(CSV_FILE, mode='x', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["FANUC LR MATE 200iB", "Time", "Current Bid"])
except FileExistsError:
    pass  # File already exists

def get_current_bid():
    try:
        # Fetch the page
        response = requests.get(URL)
        response.raise_for_status()

        # Parse the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the current bid
        bid_label = soup.find(string="Current bid:")
        if bid_label:
            bid_amount = bid_label.find_next().get_text(strip=True)
            return bid_amount
        else:
            return None
    except Exception as e:
        print(f"Error fetching bid: {e}")
        return None

# Main loop
while True:
    # Get the current bid
    current_bid = get_current_bid()

    if current_bid:
        # Log the data
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["FANUC LR MATE 200iB", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), current_bid])
        print(f"Logged: Time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Current Bid={current_bid}")
    else:
        print(f"Failed to fetch bid at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Wait for the specified interval
    time.sleep(WAIT_TIME)
