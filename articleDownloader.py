import requests
import time
import os
from datetime import datetime
# Base settings
domain = "www.darivoa.com"

# Function to validate user input
def get_valid_date(prompt):
    while True:
        user_input = input(prompt)
        
        # Ensure it's 8 digits and represents a valid date
        try:
            date_obj = datetime.strptime(user_input, "%Y%m%d")
            
            # Ensure the date is in the past
            if date_obj >= datetime.today():
                print("[ERROR] The date must be in the past.")
            else:
                return user_input + "000000"  # Append '000000' as required
        except ValueError:
            print("[ERROR] Invalid format. Please enter the date as YYYYMMDD.")

# Get user input for from and to dates
from_ts = get_valid_date("Enter the 'from' date (YYYYMMDD): ")
to_ts = get_valid_date("Enter the 'to' date (YYYYMMDD): ")
# Create a directory for today's date
today_date = datetime.today().strftime('%Y-%m-%d')
output_dir = os.path.join("downloaded_html", today_date)
os.makedirs(output_dir, exist_ok=True)

# Function to get CDX data from Wayback Machine
def get_snapshots():
    cdx_url = "https://web.archive.org/cdx/search/cdx"
    params = {
        'url': domain,
        'from': from_ts,
        'to': to_ts,
        'output': 'json'
    }

    try:
        print("Querying Wayback Machine for snapshots...")
        response = requests.get(cdx_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        if len(data) <= 1:
            print("[WARN] No snapshots found!")
            return []

        # Extract snapshots with status code 200
        snapshots = [
            {"timestamp": row[1], "original_url": row[2]}
            for row in data[1:]  # Skip header row
            if row[4] == "200"  # Only keep status 200
        ]

        print(f"Found {len(snapshots)} snapshots with status 200.")
        return snapshots

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to retrieve snapshots: {e}")
        return []

# Function to download each snapshot
def download_page(url, save_path, max_retries=3):
    for attempt in range(1, max_retries + 1):
        print(f"Downloading: {url} (Attempt {attempt})")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save HTML to file
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"Saved: {save_path}")
            
            # Wait 15 seconds before next request
            time.sleep(15)
            
            return  # Success, exit function

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] {e}")
            if attempt < max_retries:
                wait_time = 5 * attempt  # Exponential backoff (5s, 10s, 15s)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Skipping {url} after {max_retries} failed attempts.")

# Get snapshots from CDX query
snapshots = get_snapshots()

# Loop through and download snapshots
for snapshot in snapshots:
    timestamp = snapshot["timestamp"]
    original_url = snapshot["original_url"]
    
    # Construct the Wayback Machine snapshot URL
    snapshot_url = f"https://web.archive.org/web/{timestamp}if_/{original_url}"
    
    # Define file path
    save_path = os.path.join(output_dir, f"{timestamp}.html")
    
    # Download the page
    download_page(snapshot_url, save_path)
