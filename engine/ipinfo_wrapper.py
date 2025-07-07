import requests


def fetch_ipinfo(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[!] Failed to get IP info: {response.status_code}")
            return None
    except Exception as e:
        print(f"[!] Error contacting IPInfo API: {e}")
        return None