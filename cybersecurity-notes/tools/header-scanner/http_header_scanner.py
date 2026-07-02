"""
HTTP Security Header Scanner
Scans specified URLs, inspects security headers, and reports missing headers and potential risks.
"""

import requests
import json
import csv
from datetime import datetime

INFO_LEAK_HEADERS = ["Server", "X-Powered-By"]
SECURITY_HEADERS = ["Content-Security-Policy", "X-Frame-Options"]
ALL_HEADERS = INFO_LEAK_HEADERS + SECURITY_HEADERS
TIMEOUT = 10
HEADERS_TO_SEND = {
    "User-Agent": "Mozilla/5.0 (HeaderScanner/1.0; Educational)"
}


def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def scan_url(url):
    url = normalize_url(url)
    result = {
        "url": url,
        "status": None,
        "headers": {},
        "missing_security": [],
        "info_leak": [],
        "risk_level": "unknown",
        "error": None,
    }

    try:
        response = requests.get(url, headers=HEADERS_TO_SEND, timeout=TIMEOUT, allow_redirects=True)
        result["status"] = response.status_code
        result["final_url"] = response.url

        for h in ALL_HEADERS:
            value = response.headers.get(h)
            if value:
                result["headers"][h] = value

        for h in INFO_LEAK_HEADERS:
            if h in result["headers"]:
                result["info_leak"].append(h)

        for h in SECURITY_HEADERS:
            if h not in result["headers"]:
                result["missing_security"].append(h)

        result["risk_level"] = calculate_risk(result)

    except requests.exceptions.SSLError as e:
        result["error"] = f"SSL error: {e}"
    except requests.exceptions.ConnectionError:
        result["error"] = "Connection failed"
    except requests.exceptions.Timeout:
        result["error"] = f"Timeout ({TIMEOUT}s)"
    except requests.exceptions.RequestException as e:
        result["error"] = f"Request error: {e}"

    return result


def calculate_risk(result):
    missing = len(result["missing_security"])
    leaks = len(result["info_leak"])

    if missing == 0 and leaks == 0:
        return "low"
    elif missing >= 2 or (missing >= 1 and leaks >= 1):
        return "high"
    else:
        return "medium"


def print_result(result):
    risk_emoji = {"low": "✓", "medium": "⚠", "high": "✗", "unknown": "?"}
    emoji = risk_emoji.get(result["risk_level"], "?")

    print(f"\n{emoji} {result['url']}")
    print("-" * 60)

    if result["error"]:
        print(f"  ERROR: {result['error']}")
        return

    print(f"  Status: {result['status']}")
    print(f"  Risk:   {result['risk_level'].upper()}")

    if result["headers"]:
        print("\n  Found headers:")
        for k, v in result["headers"].items():
            display_v = v if len(v) < 80 else v[:77] + "..."
            print(f"    • {k}: {display_v}")

    if result["info_leak"]:
        print(f"\n  ⚠ Information leak: {', '.join(result['info_leak'])}")

    if result["missing_security"]:
        print(f"  ✗ Missing security headers: {', '.join(result['missing_security'])}")


def save_json(results, filename="scan_results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[+] JSON report saved: {filename}")


def save_csv(results, filename="scan_results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["URL", "Status", "Risk", "Server", "X-Powered-By", "CSP", "X-Frame-Options", "Missing", "Info Leak", "Error"])
        for r in results:
            h = r.get("headers", {})
            writer.writerow([
                r["url"],
                r.get("status", ""),
                r.get("risk_level", ""),
                h.get("Server", ""),
                h.get("X-Powered-By", ""),
                h.get("Content-Security-Policy", "")[:50],
                h.get("X-Frame-Options", ""),
                ", ".join(r.get("missing_security", [])),
                ", ".join(r.get("info_leak", [])),
                r.get("error", "") or "",
            ])
    print(f"[+] CSV report saved: {filename}")


def print_summary(results):
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    high = sum(1 for r in results if r.get("risk_level") == "high")
    medium = sum(1 for r in results if r.get("risk_level") == "medium")
    low = sum(1 for r in results if r.get("risk_level") == "low")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total scanned: {total}")
    print(f"  High risk:    {high}")
    print(f"  Medium risk:  {medium}")
    print(f"  Low risk:     {low}")
    print(f"  Errors:       {errors}")


def load_urls(filename):
    urls = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls


def main():
    print("=" * 60)
    print("HTTP SECURITY HEADER SCANNER")
    print("=" * 60)

    print("\n  1) Load URLs from file (urls.txt)")
    print("  2) Enter a URL manually")
    secim = input("\nSelection: ").strip()

    if secim == "1":
        try:
            urls = load_urls("urls.txt")
            print(f"\n[+] {len(urls)} URLs loaded.")
        except FileNotFoundError:
            print("[!] urls.txt not found. Switching to manual input.")
            urls = [input("URL: ").strip()]
    else:
        urls = [input("URL: ").strip()]

    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Scanning: {url}")
        result = scan_url(url)
        print_result(result)
        results.append(result)

    print_summary(results)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(results, f"scan_{timestamp}.json")
    save_csv(results, f"scan_{timestamp}.csv")


if __name__ == "__main__":
    main()
