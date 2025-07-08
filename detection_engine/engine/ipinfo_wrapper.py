# ipinfo_wrapper.py
# --------------------------------------------------
# Fetches metadata for a given IP address from IPInfo.
# Returns structured data including location, ASN, and coordinates
# for use in both CLI and web-based VPN detection.
# --------------------------------------------------

import requests

def fetch_ipinfo(ip):
    """
    Contacts the IPInfo API and extracts relevant IP metadata.

    Args:
        ip (str): The IP address to query.

    Returns:
        dict: {
            ip (str),
            org (str),
            asn (str),
            location (str),
            latitude (float),
            longitude (float)
        }
    """
    url = f"https://ipinfo.io/{ip}/json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"[!] Failed to get IP info: {response.status_code}")
            return None

        data = response.json()

        # Extract standard fields
        ip_address = data.get("ip")
        org_info = data.get("org", "")
        asn = org_info.split()[0] if org_info else None

        # Extract and safely join location fields
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")
        location = ", ".join(part for part in [city, region, country] if part) or "Unknown"

        # Extract lat/lon from 'loc' string (e.g., "47.6104,-122.2007")
        loc = data.get("loc")
        latitude, longitude = None, None
        if loc:
            try:
                latitude, longitude = map(float, loc.split(","))
            except ValueError:
                pass  # leave lat/lon as None if malformed

        # Build final result
        return {
            "ip": ip_address,
            "org": org_info,
            "asn": asn,
            "location": location,
            "latitude": latitude,
            "longitude": longitude
        }

    except Exception as e:
        print(f"[!] Error contacting IPInfo API: {e}")
        return None