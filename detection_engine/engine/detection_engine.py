from .ipinfo_wrapper import fetch_ipinfo
from .heuristics import analyze_with_heuristics
from .abuseipdb_checker import check_abuseipdb
from .ipqualityscore_checker import check_ipqs

# This is the core detection engine. It pulls IP metadata, applies heuristics,
# queries external APIs (if configured), and returns a unified result with scoring and context.

def detect_ip(ip):
    # Step 1: Fetch IP metadata (org, ASN, location)
    data = fetch_ipinfo(ip)
    if not data:
        return {"error": "Failed to retrieve IP data."}
    
    # Step 2: Apply heuristic rules based on org name and ASN
    verdict, reason = analyze_with_heuristics(data)

    # Step 3: Check IP reputation via AbuseIPDB and IPQualityScore (optional)
    abuse_data = check_abuseipdb(ip)
    ipqs_data = check_ipqs(ip)

    # Extract org name and ASN neatly from IPInfo
    org_raw = data.get("org", "")
    asn = org_raw.split()[0] if org_raw.startswith("AS") else "N/A"
    org_name = " ".join(org_raw.split()[1:]) if asn != "N/A" else org_raw
    location = f"{data.get('city', '')}, {data.get('country', '')}"

    # Parse scores from APIs (handle fallback safely)
    abuse_score = abuse_data.get("abuseConfidenceScore", 0)
    fraud_score = ipqs_data.get("fraud_score", 0)
    try:
        abuse_score = int(abuse_score)
        fraud_score = int(fraud_score)
    except:
        abuse_score = 0
        fraud_score = 0

     # Step 4: Determine confidence level based on scores
    if abuse_score >= 90 or fraud_score >= 90:
        confidence = "High"
    elif abuse_score >= 50 or fraud_score >= 50:
        confidence = "Moderate"
    else:
        confidence = "Low"

    # Step 5: Finalize results with a disclaimer
    disclaimer = (
        "This result indicates whether the IP shows characteristics of VPN/proxy or abusive usage. "
        "It does not imply malicious intent. Many users use VPNs for privacy or remote work."
    )

    # Return full structured detection result
    return {
        "ip": ip,
        "org": org_name,
        "asn": asn,
        "location": location,
        "is_suspicious": verdict or ipqs_data.get("vpn", False),
        "detection_reason": reason if verdict else ipqs_data.get("reason", "None"),
        "abuse_score": abuse_score,
        "ipqs_fraud_score": fraud_score,
        "confidence_level": confidence,
        "disclaimer": disclaimer
    }
