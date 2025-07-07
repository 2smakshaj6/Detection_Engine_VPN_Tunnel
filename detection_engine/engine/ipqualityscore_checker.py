import requests
import os

# Module to check IP against IPQualityScore VPN/Proxy/Fraud APIs

api_key = os.getenv("IPQUALITYSCORE_API_KEY")

API_URL = "https://ipqualityscore.com/api/json/ip/{}"  # Format with API key

def check_ipqs(ip):
    if not api_key:
        return {}

    try:
        full_url = f"{API_URL.format(api_key)}/{ip}"
        response = requests.get(full_url, timeout=10)
        return response.json()
    except Exception:
        return {}