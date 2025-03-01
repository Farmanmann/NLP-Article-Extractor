import requests

#Tests for all availible articles, gets status codes of each to verify all the articles that can be extracted.



domain = "www.darivoa.com"  # or "darivoa.com"
from_ts = "20250210000000"
to_ts   = "20250223000000"

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
