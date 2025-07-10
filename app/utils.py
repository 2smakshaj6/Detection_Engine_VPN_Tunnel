# Contains helper functions for file uploads, IP resolution, and breach checks
import os
import requests

def parse_file(file):
    # Parses a .txt or .csv file and returns a list of IPs
    lines = file.read().decode('utf-8').splitlines()
    return [line.strip() for line in lines if line.strip()]

def get_client_ip(request):
    # Retrieves the real client IP address even behind proxies like Vercel
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.remote_addr

def check_hibp(email):
    # Queries HaveIBeenPwned API for a given email address
    hibp_key = os.getenv("HIBP_API_KEY")
    if not hibp_key:
        return {"error": "HIBP API key missing."}

    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": hibp_key,
        "user-agent": "vpn-detector"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            return []  # No breach found
        else:
            return {"error": f"HIBP Error: {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}