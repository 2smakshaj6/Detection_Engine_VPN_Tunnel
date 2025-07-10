import requests
import json
from datetime import datetime
from pathlib import Path

# Threat feed URLs
FEEDS = {
    "tor": "https://check.torproject.org/exit-addresses",
    "botnet": [
        "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
        "https://sslbl.abuse.ch/blacklist/sslipblacklist.txt"
    ],
    "ddos": [
        "https://iplists.firehol.org/files/firehol_level3.netset"
    ],
    "drop": [
        "https://www.spamhaus.org/drop/drop.txt"
    ]
}

# Local output file
OUTPUT_PATH = Path(__file__).resolve().parent / "engine" / "known_bad_ips.json"


def extract_ips_from_text(text):
    lines = text.splitlines()
    return [line.strip().split()[0] for line in lines if line and not line.startswith("#")]


def fetch_feed(name, urls):
    ips = set()
    if isinstance(urls, str):
        urls = [urls]

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                if name == "tor":
                    # Tor exit nodes require special parsing
                    for line in response.text.splitlines():
                        if line.startswith("ExitAddress"):
                            ip = line.split()[1]
                            ips.add(ip)
                else:
                    ips.update(extract_ips_from_text(response.text))
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return list(ips)


def update_known_bad_ips():
    all_data = {}
    for category, urls in FEEDS.items():
        print(f"Fetching {category} feed(s)...")
        all_data[category] = fetch_feed(category, urls)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"Updated known_bad_ips.json with {sum(len(v) for v in all_data.values())} entries")


if __name__ == "__main__":
    update_known_bad_ips()