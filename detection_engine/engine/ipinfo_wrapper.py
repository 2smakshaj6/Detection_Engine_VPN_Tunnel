import requests

def fetch_ipinfo(ip):
    url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[!] Failed to get IP info: {response.status_code}")
            return None

        data = response.json()

        # Start building result with core info
        result = {
            "ip": data.get("ip"),
            "org": data.get("org"),
            "asn": data.get("org", "").split()[0] if "org" in data else None,
            "location": f"{data.get('city', '')}, {data.get('region', '')}, {data.get('country', '')}".strip(", ")
        }

        # Extract latitude and longitude if available
        loc = data.get("loc")  # e.g., "37.3860,-122.0840"
        if loc:
            try:
                lat, lon = map(float, loc.split(","))
                result["latitude"] = lat
                result["longitude"] = lon
            except ValueError:
                result["latitude"] = None
                result["longitude"] = None
        else:
            result["latitude"] = None
            result["longitude"] = None

        return result

    except Exception as e:
        print(f"[!] Error contacting IPInfo API: {e}")
        return None