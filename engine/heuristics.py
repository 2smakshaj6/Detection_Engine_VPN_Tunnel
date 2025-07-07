import json
import os

# This module handles heuristic analysis of IP metadata.
# It checks ASN numbers and organization names for signs of VPN, proxy, or hosting behavior.

SUSPICIOUS_ASN_PATH = os.path.join("config", "suspicious_asns.json")

# Load suspicious ASN list from JSON
with open(SUSPICIOUS_ASN_PATH, "r") as file:
    SUSPICIOUS_ASNS = [entry["asn"] for entry in json.load(file)]

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
    "cloud": 2
}


def analyze_with_heuristics(ip_data):
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
