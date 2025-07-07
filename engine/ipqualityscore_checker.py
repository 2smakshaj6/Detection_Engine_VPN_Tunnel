import os
import requests

def check_ipqs(ip):
    api_key = "pyTAgQWOY4nQMYnyeDdAO28jnG6URVwu"
    if not api_key:
        return {}

    try:
        response = requests.get(
            f"https://ipqualityscore.com/api/json/ip/{api_key}/{ip}"
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "vpn": data.get("vpn"),
                "fraud_score": data.get("fraud_score"),
                "reason": "Flagged as VPN/Proxy by IPQualityScore" if data.get("vpn") else "Not flagged"
            }
    except Exception as e:
        print(f"[!] IPQualityScore error: {e}")
    return {}