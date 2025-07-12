# threat_feeds.py
# -----------------------------------------------
# Loads threat intel data from known_bad_ips.json
# and flattens it for real-time IP checking.
# -----------------------------------------------

import json
import os
from datetime import datetime, timedelta

# Local path to your grouped feed file
CACHE_FILE = os.path.join(os.path.dirname(__file__), 'known_bad_ips.json')
REFRESH_INTERVAL_HOURS = 24

def flatten_grouped_ips(grouped_data):
    """Flatten {category: [ips]} into {ip: category}."""
    flat_map = {}
    for category, ip_list in grouped_data.items():
        if isinstance(ip_list, list):
            for ip in ip_list:
                flat_map[ip] = category
    return flat_map

def load_threat_data():
    """Loads and flattens the known_bad_ips.json threat intel file."""
    if not os.path.exists(CACHE_FILE):
        raise FileNotFoundError(f"[ERROR] Cache file {CACHE_FILE} not found.")

    with open(CACHE_FILE, 'r') as f:
        grouped_data = json.load(f)

    return flatten_grouped_ips(grouped_data)

def is_ip_in_threat_feeds(ip):
    try:
        bad_ips = load_threat_data()
        if ip in bad_ips:
            return [bad_ips[ip]]  # Return category match as a list
    except Exception as e:
        print(f"[WARN] Threat feed check failed: {e}")
    return []