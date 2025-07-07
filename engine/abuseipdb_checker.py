import requests
import os

# Module to check an IP against AbuseIPDB reputation score

api_key = os.getenv("ABUSEIPDB_API_KEY")

API_URL = "https://api.abuseipdb.com/api/v2/check"

def check_abuseipdb(ip):
    if not api_key:
        return {}

    try:
        headers = {
            "Key": api_key,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip,
            "maxAgeInDays": "90"
        }
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        data = response.json()
        return data.get("data", {})
    except Exception:
        return {}