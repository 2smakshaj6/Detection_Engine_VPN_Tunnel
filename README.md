# Detection Engine – Web Interface

This is a personal project built to help identify whether an IP address is likely associated with a VPN, proxy, or other suspicious behavior. It offers a simple web interface that combines IP metadata, public API reputation scores, and custom heuristics to provide helpful context about a given IP.

## What This Project Does

- Allows you to check any IP address for suspicious characteristics
- Displays organization, ASN, and geolocation data
- Shows a confidence level based on multiple detection signals
- Visualizes the IP’s location on a map and provides a reputation score meter
- Offers a "What's My IP" button to instantly analyze your own IP
- Optionally integrates with IPQualityScore and AbuseIPDB APIs for advanced results

## Who This Is For

This tool is ideal for:

- Security enthusiasts and researchers
- Developers building IP intelligence systems
- Anyone curious about who might be behind a particular IP
- Privacy-conscious individuals

It’s meant to be a helpful, transparent starting point—not a definitive label for good or bad actors.

## How to Use

1. Visit the web interface
2. Enter any IP address you want to investigate
3. Click “Check IP”
4. You’ll see a summary including ISP, location, ASN, and any red flags
5. Optionally click “What’s My IP” to check your current IP address

## Powered by a Python Module

This web interface runs on top of a Python detection engine that you can install and use in your own projects:

```bash
pip install detection_engine
```

Then in your code:

```python
from detection_engine import detect_ip

detect_ip("8.8.8.8")
```

The backend uses IPInfo for IP metadata and can optionally pull abuse and fraud scores from third-party services if API keys are configured.

## Technologies Used

- Python (Flask)
- HTML and CSS (no frameworks)
- IPInfo, IPQualityScore, and AbuseIPDB (for metadata and scores)
- Google Maps (for visualization)

## Project Status

This project is still under development. More features will be added in future updates, including:

- Batch IP uploads (CSV or TXT)
- Breach email lookups
- Dark mode and accessibility enhancements

## License

This project is open source under the MIT license. Use it however you like, with or without changes.

## A Note from the Developer

This started as a curiosity-driven weekend project. It’s not perfect, but it’s designed to be honest, educational, and practical. I’m open to suggestions, improvements, or just hearing what you think.