import argparse
from detection_engine.engine.detection_engine import detect_ip
from tqdm import tqdm
import time

def show_loading():
    print("\n------------------------ Welcome to the VPN & Threat Detection CLI Tool ------------------------")
    print("\nThis tool checks if an IP address is associated with VPNs, proxies, abuse sources, or threat feeds (e.g. Tor, Botnets).")
    print("It uses heuristics, APIs, and auto-updated IP threat feeds for comprehensive detection.\n")
    tqdm.write("You can cancel the operation at any time by pressing Ctrl+C.\n")
    tqdm.write("Starting the detection process...\n")
    for _ in tqdm(range(50), desc="Analyzing IP", ncols=75):
        time.sleep(0.01)

def print_result(result):
    print("\nDetection Result")
    print("------------------")

    fields = {
        "ip": "IP",
        "org": "ORG",
        "asn": "ASN",
        "location": "Location",
        "is_suspicious": "Is Suspicious",
        "detection_reason": "Detection Reason",
        "abuse_score": "Abuse Score",
        "ipqs_fraud_score": "IPQS Fraud Score",
        "confidence_level": "Confidence Level",
        "disclaimer": "Disclaimer"
    }

    for key, label in fields.items():
        val = result.get(key, "N/A")
        if key == "is_suspicious":
            val = "Yes" if val else "No"
        print(f"{label:<18}: {val}")

    # Show threat feed matches if present
    feed_matches = result.get("threat_feed_matches", [])
    if feed_matches:
        print("\nThreat Feed Matches")
        print("--------------------")
        for source in feed_matches:
            print(f"✔ {source}")
    else:
        print("\nThreat Feed Matches")
        print("--------------------")
        print("No matches found in known threat feeds.")


def main():
    parser = argparse.ArgumentParser(description="Detect VPN, Proxy, Botnet, and Abuse IPs")
    parser.add_argument("--ip", required=True, help="IP address to analyze")
    args = parser.parse_args()

    show_loading()
    result = detect_ip(args.ip)

    if result.get("error"):
        print(f"\n[!] Error: {result['error']}")
    else:
        print_result(result)


if __name__ == "__main__":
    main()