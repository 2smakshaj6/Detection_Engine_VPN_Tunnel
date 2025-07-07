import argparse
from detection_engine.engine.detection_engine import detect_ip
from tqdm import tqdm
import time

# This is the main CLI entry point that takes an IP address, shows a loading bar,
# fetches detection results from the engine, and prints them cleanly to the terminal.

def show_loading():
    # Simulates a loading progress bar while the detection is running
    print("\n-------------------------- Welcome to the VPN & Tunnel Detection CLI Tool --------------------------")
    print("\nThis tool checks if an IP address is associated with VPN, proxy, or tunneling services.")
    print("It uses multiple data sources to provide a comprehensive analysis.\n")
    tqdm.write("You can cancel the operation at any time by pressing Ctrl+C.\n")
    tqdm.write("Starting the detection process...\n")
    for _ in tqdm(range(50), desc="Analyzing IP", ncols=75):
        time.sleep(0.01)


def print_result(result):
    # Neatly prints all detection results in a formatted way
    print("\nDetection Result")
    print("------------------")
    for key in [
        "ip", "org", "asn", "location",
        "is_suspicious", "detection_reason",
        "abuse_score", "ipqs_fraud_score",
        "confidence_level", "disclaimer"]:
        value = result.get(key, "N/A")
        label = key.replace("_", " ").upper()
        if key == "is_suspicious":
            value = "Yes" if value else "No"
        print(f"{label:<18}: {value}")


def main():
    # Parse CLI arguments and trigger detection
    parser = argparse.ArgumentParser(description="VPN & Tunnel Detection CLI Tool")
    parser.add_argument("--ip", required=True, help="Enter the IP address to check")
    args = parser.parse_args()

    show_loading()
    result = detect_ip(args.ip)
    print_result(result)


if __name__ == "__main__":
    main()