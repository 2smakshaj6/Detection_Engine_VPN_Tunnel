# threat_feeds.py
# -----------------------------------------------
# Fetches, caches, and checks known bad IPs from
# public threat feeds (botnet C2, Tor nodes, DDoS infra).
# Auto-refresh supported for daily updates.
# -----------------------------------------------

import requests
import os
import json
from datetime import datetime, timedelta

# Path to local threat cache
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'known_bad_ips.json')
REFRESH_INTERVAL_HOURS = 24

# Public threat sources
THREAT_FEEDS = {
    "Botnet C2": "https://raw.githubusercontent.com/stamparm/maltrail/master/trails/static/malware/botnet.txt",
    "Tor Exit Nodes": "https://check.torproject.org/exit-addresses",
    # Add more if needed
}

def fetch_threat_data():
    print("[INFO] Refreshing threat intelligence feeds...")
    threat_data = {"metadata": {"updated": datetime.utcnow().isoformat()}, "ips": {}}

    for category, url in THREAT_FEEDS.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                lines = response.text.splitlines()
                for line in lines:
                    line = line.strip()
                    if category == "Tor Exit Nodes" and line.startswith("ExitAddress"):
                        ip = line.split()[1]
                        threat_data["ips"][ip] = category
                    elif line and not line.startswith("#") and category != "Tor Exit Nodes":
                        ip = line.split()[0]
                        threat_data["ips"][ip] = category
        except Exception as e:
            print(f"[WARN] Failed to fetch {category} feed: {e}")

    # Save to disk
    with open(CACHE_FILE, 'w') as f:
        json.dump(threat_data, f, indent=2)

def load_threat_data():
    if not os.path.exists(CACHE_FILE):
        fetch_threat_data()

    with open(CACHE_FILE, 'r') as f:
        data = json.load(f)

    # Refresh cache if too old
    last_updated = datetime.fromisoformat(data.get('metadata', {}).get('updated', '2000-01-01T00:00:00'))
    if datetime.utcnow() - last_updated > timedelta(hours=REFRESH_INTERVAL_HOURS):
        fetch_threat_data()
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)

    return data.get('ips', {})

def is_ip_in_threat_feeds(ip):
    bad_ips = load_threat_data()
    if ip in bad_ips:
        return [bad_ips[ip]]
    return []