# detection_engine.py
# ---------------------------------------------------
# This is the core detection engine that coordinates all checks:
# 1. Fetches IP metadata (IPInfo)
# 2. Applies heuristic rules (suspicious ASNs or orgs)
# 3. Pulls reputation scores from AbuseIPDB and IPQualityScore (optional)
# 4. Checks against known bad IP feeds (Tor, Botnet, DDoS, Spamhaus, etc)
# 5. Returns a structured result with confidence scoring
# ---------------------------------------------------

from .ipinfo_wrapper import fetch_ipinfo
from .heuristics import analyze_with_heuristics
from .abuseipdb_checker import check_abuseipdb
from .ipqualityscore_checker import check_ipqs
from .threat_feeds import is_ip_in_threat_feeds

def detect_ip(ip):
    # Step 1: Fetch metadata from IPInfo
    data = fetch_ipinfo(ip)
    if not data:
        return {"error": "Failed to retrieve IP data."}

    # Step 2: Apply heuristic analysis based on ASN and org
    is_suspicious, reason = analyze_with_heuristics(data)

    # Step 3: Optional — check external reputation scores
    abuse_data = check_abuseipdb(ip)
    ipqs_data = check_ipqs(ip)

    # Step 4: Check threat intelligence feeds (botnets, Tor, DDoS, Spamhaus, etc.)
    threat_matches = is_ip_in_threat_feeds(ip)
    if threat_matches:
        is_suspicious = True
        reason = f"Flagged in threat feeds: {', '.join(threat_matches)}"

    # Step 5: Extract and clean organization details
    org_raw = data.get("org", "")
    asn = org_raw.split()[0] if org_raw.startswith("AS") else "N/A"
    org_name = " ".join(org_raw.split()[1:]) if asn != "N/A" else org_raw

    # Use already-cleaned location string from ipinfo_wrapper.py
    location = data.get("location", "Unknown")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # Step 6: Normalize reputation scores
    try:
        abuse_score = int(abuse_data.get("abuseConfidenceScore", 0))
    except (TypeError, ValueError):
        abuse_score = 0

    try:
        fraud_score = int(ipqs_data.get("fraud_score", 0))
    except (TypeError, ValueError):
        fraud_score = 0

    # Step 7: Determine confidence level
    if abuse_score >= 90 or fraud_score >= 90:
        confidence = "High"
    elif abuse_score >= 50 or fraud_score >= 50:
        confidence = "Moderate"
    else:
        confidence = "Low"

    # Final message to remind users of proper context
    disclaimer = (
        "This result indicates whether the IP shows characteristics of VPN/proxy, abuse, or known threat activity. "
        "It does not imply malicious intent. Many users use VPNs for privacy or remote work."
    )

    # Step 8: Return structured result
    return {
        "ip": ip,
        "org": org_name,
        "asn": asn,
        "location": location,
        "latitude": latitude,
        "longitude": longitude,
        "is_suspicious": is_suspicious or ipqs_data.get("vpn", False),
        "detection_reason": reason if is_suspicious else ipqs_data.get("reason", "None"),
        "abuse_score": abuse_score,
        "ipqs_fraud_score": fraud_score,
        "confidence_level": confidence,
        "disclaimer": disclaimer,
        "threat_feed_matches": threat_matches if threat_matches else []
    }