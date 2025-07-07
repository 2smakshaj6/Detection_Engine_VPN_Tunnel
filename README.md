# VPN & Tunnel Detection CLI Tool
[![PyPI version](https://img.shields.io/pypi/v/detection_engine)](https://pypi.org/project/detection_engine/)
[![Python version](https://img.shields.io/pypi/pyversions/detection_engine)](https://pypi.org/project/detection_engine/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/detection_engine)](https://pepy.tech/project/detection_engine)

[![PyPI version](https://img.shields.io/pypi/v/detection_engine)](https://pypi.org/project/detection_engine/)
[![Python version](https://img.shields.io/pypi/pyversions/detection_engine)](https://pypi.org/project/detection_engine/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/detection_engine)](https://pepy.tech/project/detection_engine)

This project is a Python-based command-line tool that helps you detect whether an IP address is likely coming from a VPN, proxy, or abusive source. It uses a combination of IP metadata, ASN heuristics, and optional third-party API lookups for deeper inspection.

---

## Features
- Checks organization name and ASN for suspicious patterns
- Uses IPInfo (free) for geolocation and org info
- Integrates with [AbuseIPDB](https://www.abuseipdb.com/) and [IPQualityScore](https://ipqualityscore.com/) APIs for reputation checks (optional)
- Heuristic-based scoring system with confidence levels (Low / Moderate / High)
- CLI-based tool installable with `pip install` + global command `vpnscan`

---

## Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/vpn-tunnel-detector.git
cd vpn-tunnel-detector
```

2. Set up a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the module in editable mode:
```bash
pip install --editable .
```

This registers the `vpnscan` command globally in your environment.

---

## API Keys (Optional, for advanced detection)
To enhance detection accuracy with threat intelligence data, you can provide your own API keys for:
- **AbuseIPDB** (IP reputation reports)
- **IPQualityScore** (VPN/proxy/fraud scoring)

Instead of hardcoding your API keys, we recommend using a `.env` file for safety:

### How to set up your `.env` file:
1. Create a copy of the example file:
```bash
cp .env.example .env
```
2. Edit `.env` and paste your actual keys:
```
ABUSEIPDB_API_KEY=your_abuseipdb_key
IPQUALITYSCORE_API_KEY=your_ipqs_key
```

We automatically load these with `os.getenv(...)`. No secrets are stored in the codebase.

---

## Usage
Run the tool using:
```bash
vpnscan --ip <IP_ADDRESS>
```
Example:
```bash
vpnscan --ip 104.28.228.78
```

You’ll see output like this:
```
-------------------------- Welcome to the VPN & Tunnel Detection CLI Tool --------------------------

This tool checks if an IP address is associated with VPN, proxy, or tunneling services.
It uses multiple data sources to provide a comprehensive analysis.

You can cancel the operation at any time by pressing Ctrl+C.

Starting the detection process...

Analyzing IP: 100%|████████████████████████| 50/50 [00:00<00:00, 82.80it/s]

Detection Result
------------------
IP                : 104.28.228.78
ORG               : Cloudflare, Inc.
ASN               : AS13335
LOCATION          : Washington, US
IS SUSPICIOUS     : Yes
DETECTION REASON  : ASN AS13335 is frequently used by VPN or hosting providers. Org name includes 'cloud', commonly seen in VPN or hosting services.
ABUSE SCORE       : 100
IPQS FRAUD SCORE  : 100
CONFIDENCE LEVEL  : High
DISCLAIMER        : This result indicates whether the IP shows characteristics of VPN/proxy or abusive usage. It does not imply malicious intent. Many users use VPNs for privacy or remote work.
```
---

## Project Structure
```
detection_engine/
├── engine/
│   ├── ipinfo_wrapper.py
│   ├── heuristics.py
│   ├── detection_engine.py
│   ├── abuseipdb_checker.py
│   └── ipqualityscore_checker.py
├── config/
│   └── suspicious_asns.json
├── run_engine.py
├── requirements.txt
└── README.md
```

---

## License
MIT License — free to use and modify with attribution.
