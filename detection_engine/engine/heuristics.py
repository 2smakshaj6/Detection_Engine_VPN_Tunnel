# This module applies heuristic rules to detect suspicious ASNs and org names

import json
import importlib.resources

# Define keyword scores to assess organization names
KEYWORD_SCORES = {
    "vpn": 4,
    "proxy": 4,
    "anonymous": 4,
    "tor": 3,
    "exit": 3,
    "hosting": 3,
    "server": 3,
    "colo": 3,
    "cloud": 2,
    "dedicated": 2,
    "vps": 3,
    "tunnel": 3,
    "datacenter": 3,
    "ssh": 2,
    "rented": 2,
    "infra": 2,
    "host": 2
}


def load_suspicious_asns():
    """Load the suspicious ASN list from packaged JSON data."""
    with importlib.resources.files("detection_engine.config").joinpath("suspicious_asns.json").open("r") as file:
        return [entry["asn"] for entry in json.load(file)]


SUSPICIOUS_ASNS = load_suspicious_asns()


def analyze_with_heuristics(ip_data):
    """
    Analyze IP metadata using a score-based heuristic:
    - ASN matches known suspicious list
    - Org name contains keywords like 'vpn', 'proxy', etc.
    """
    org = ip_data.get("org", "").lower()
    asn = ip_data.get("org", "").split()[0].upper() if "org" in ip_data else "N/A"

    score = 0
    reasons = []

    if asn in SUSPICIOUS_ASNS:
        score += 5
        reasons.append(f"ASN {asn} is known for hosting or VPN-related traffic.")

    for keyword, weight in KEYWORD_SCORES.items():
        if keyword in org:
            score += weight
            reasons.append(f"Organization name includes '{keyword}', commonly used in VPN/proxy infrastructure.")

    if score >= 5:
        return True, " ".join(reasons)
    else:
        return False, "No strong indicators of VPN or tunneling activity."
