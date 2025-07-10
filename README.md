# Detection Engine – Web Interface

This is a simple project I built to help check whether an IP address might be using a VPN, proxy, Tor exit node, or be involved in suspicious activity. It’s powered by a Python backend and offers a clean web interface to explore IP intelligence in real time.

---

## What It Does

- Looks up IP addresses for red flags like VPNs, hosting services, Tor nodes, or botnet infrastructure
- Uses IP metadata (like ISP, location, and ASN) to detect patterns
- Checks against known abuse and fraud databases (optional)
- Shows a confidence score based on combined signals
- Maps the IP’s location using Google Maps
- Includes a basic risk meter and an easy “What’s My IP” tool
- Lets you flag any IP manually for review

---

## Who It's For

This tool is meant for:

- Cybersecurity beginners or enthusiasts
- Developers building tools with IP context
- Anyone curious about who’s behind an IP address
- Privacy-aware users wanting to check their own IP

It’s not meant to judge good vs. bad — just to provide useful insights.

---

## How to Use It

1. Visit the web interface (hosted on Vercel)
2. Enter an IP address you want to check
3. Click “Check IP” to get a full report
4. You can also hit “What’s My IP” to analyze your current IP
5. Optionally, flag any IP you find suspicious

---

## Use the Engine in Your Own Code

The backend logic is available as a Python package. To install:

```bash
pip install detection_engine
```

To use it:

```python
from detection_engine import detect_ip
detect_ip("8.8.8.8")
```

This returns a dictionary of results you can use however you want.

---

## Tor Node Check (Manual)

Want to check if an IP is part of the Tor exit node network?

You can do this with:

```bash
curl -s https://check.torproject.org/exit-addresses | grep "^ExitAddress"   
```

Replace `<ip-address>` with any IP you want to check. If it’s listed, you’ll see a match.

---

## Generate a Secret Key

For your Flask app, you’ll need a secure secret key. You can create one like this:

```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then add it to your `.env` file and your Vercel environment settings:

```
SECRET_KEY=your-long-random-string
```

---

## File Structure

```
deteng_web/
├── app/
│   ├── __init__.py               # App factory and config
│   ├── routes.py                 # All Flask routes
│   ├── utils.py                  # Helper functions (file parsing, IP, breach check)
│   ├── templates/                # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── result.html
│   │   └── batch_result.html
│   └── static/                   # Static files (CSS, images)
│       ├── css/
│       │   └── styles.css
│       └── img/
│           └── image.png
├── uploads/                      # Stores uploaded .txt/.csv files
├── index.py                      # App entry point
├── .env                          # Environment variables (not committed)
├── .env.example                  # Example env for setup
├── flagged_ips.txt              # IPs manually flagged from the site
├── .gitignore
├── .vercelignore
├── requirements.txt             # Python dependencies
├── vercel.json                  # Vercel configuration
└── README.md
```

---

## What’s Next

This is still a work-in-progress. Here’s what’s coming soon:

- Batch IP scanning from TXT or CSV files
- Email breach check using HaveIBeenPwned
- Dark mode and UI polish
- Safer flagging and logging features
- And many more updates....!

---

## License

MIT License — feel free to use, remix, or build on top of it.

---

## A Personal Note

I started this project as a weekend experiment, and it’s grown into something I actually use and enjoy building. It’s still improving, but I wanted to share it early. If it’s helpful, feel free to fork or suggest improvements. I’m open to feedback.