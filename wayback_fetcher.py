import requests
from datetime import datetime

#Tests for all availible articles, gets status codes of each to verify all the articles that can be extracted.



domain = "www.darivoa.com"  # or "darivoa.com"

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



params = {
    'url': domain,
    'from': from_ts,
    'to': to_ts,
    'output': 'json'
}

r = requests.get("https://web.archive.org/cdx/search/cdx", params=params, timeout=30)
print("CDX query URL:", r.url)

if r.status_code == 200:
    lines = r.text.strip().split('\n')
    if len(lines) > 1:
        print("[INFO] Found snapshots:")
        print("\n".join(lines[:10]))  # show first 10 lines
    else:
        print("[WARN] No data lines found.")
else:
    print(f"[ERROR] {r.status_code} {r.text}")
