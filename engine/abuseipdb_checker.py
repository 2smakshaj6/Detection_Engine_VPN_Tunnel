import os
import requests

def check_abuseipdb(ip):
    api_key = "b6b2ac2e75f2be2481d9bb764d5b101e14bfa1609174edba2b2a59ec83d5813f3dd27c818b10765b"
    if not api_key:
        return {}

    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers={"Key": api_key, "Accept": "application/json"},
            params={"ipAddress": ip, "maxAgeInDays": "90"}
        )
        if response.status_code == 200:
            return response.json().get("data", {})
    except Exception as e:
        print(f"[!] AbuseIPDB error: {e}")
    return {}