"""
HTTP Security Header Scanner
Belirtilen URL'leri tarar, güvenlik header'larını kontrol eder ve eksik
olanları potansiyel risk olarak raporlar.
"""

import requests
import json
import csv
from datetime import datetime
from urllib.parse import urlparse

# ---------- Yapılandırma ----------

# Bilgi sızdıran header'lar (varsa risk)
INFO_LEAK_HEADERS = ["Server", "X-Powered-By"]

# Olması gereken güvenlik header'ları (yoksa risk)
SECURITY_HEADERS = ["Content-Security-Policy", "X-Frame-Options"]

# Tüm ilgilendiğimiz header'lar
ALL_HEADERS = INFO_LEAK_HEADERS + SECURITY_HEADERS

# requests timeout (saniye)
TIMEOUT = 10

# User-Agent: bazı siteler default Python UA'yı bloklar
HEADERS_TO_SEND = {
    "User-Agent": "Mozilla/5.0 (HeaderScanner/1.0; Educational)"
}

# ---------- Çekirdek fonksiyonlar ----------

def normalize_url(url):
    """URL şeması yoksa https ekler."""
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url

def scan_url(url):
    """Tek bir URL'yi tarar ve sonuç sözlüğü döner."""
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
        # allow_redirects=True → 301/302 takip et, son sayfayı analiz et
        response = requests.get(
            url,
            headers=HEADERS_TO_SEND,
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        result["status"] = response.status_code
        result["final_url"] = response.url  # redirect olduysa son URL

        # İlgilendiğimiz header'ları topla
        for h in ALL_HEADERS:
            value = response.headers.get(h)
            if value:
                result["headers"][h] = value

        # Bilgi sızıntısı kontrolü
        for h in INFO_LEAK_HEADERS:
            if h in result["headers"]:
                result["info_leak"].append(h)

        # Eksik güvenlik header'ı kontrolü
        for h in SECURITY_HEADERS:
            if h not in result["headers"]:
                result["missing_security"].append(h)

        # Risk seviyesi kararı
        result["risk_level"] = calculate_risk(result)

    except requests.exceptions.SSLError as e:
        result["error"] = f"SSL hatası: {e}"
    except requests.exceptions.ConnectionError:
        result["error"] = "Bağlantı kurulamadı"
    except requests.exceptions.Timeout:
        result["error"] = f"Timeout ({TIMEOUT}s)"
    except requests.exceptions.RequestException as e:
        result["error"] = f"İstek hatası: {e}"

    return result

def calculate_risk(result):
    """Basit bir risk skorlama mantığı."""
    missing = len(result["missing_security"])
    leaks = len(result["info_leak"])

    if missing == 0 and leaks == 0:
        return "low"
    elif missing >= 2 or (missing >= 1 and leaks >= 1):
        return "high"
    else:
        return "medium"

# ---------- Çıktı / Raporlama ----------

def print_result(result):
    """Tek bir sonucu konsola güzel formatta yazdırır."""
    risk_emoji = {
        "low": "✓",
        "medium": "⚠",
        "high": "✗",
        "unknown": "?",
    }
    emoji = risk_emoji.get(result["risk_level"], "?")

    print(f"\n{emoji} {result['url']}")
    print("-" * 60)

    if result["error"]:
        print(f"  HATA: {result['error']}")
        return

    print(f"  Status: {result['status']}")
    print(f"  Risk:   {result['risk_level'].upper()}")

    if result["headers"]:
        print("\n  Bulunan header'lar:")
        for k, v in result["headers"].items():
            display_v = v if len(v) < 80 else v[:77] + "..."
            print(f"    • {k}: {display_v}")

    if result["info_leak"]:
        print(f"\n  ⚠ Bilgi sızıntısı: {', '.join(result['info_leak'])}")

    if result["missing_security"]:
        print(f"  ✗ Eksik güvenlik header'ı: {', '.join(result['missing_security'])}")

def save_json(results, filename="scan_results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n[+] JSON raporu kaydedildi: {filename}")

def save_csv(results, filename="scan_results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "URL", "Status", "Risk", "Server", "X-Powered-By",
            "CSP", "X-Frame-Options", "Missing", "Info Leak", "Error"
        ])
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
    print(f"[+] CSV raporu kaydedildi: {filename}")

def print_summary(results):
    """Toplu özet."""
    total = len(results)
    errors = sum(1 for r in results if r.get("error"))
    high = sum(1 for r in results if r.get("risk_level") == "high")
    medium = sum(1 for r in results if r.get("risk_level") == "medium")
    low = sum(1 for r in results if r.get("risk_level") == "low")

    print("\n" + "=" * 60)
    print("ÖZET")
    print("=" * 60)
    print(f"  Toplam taranan: {total}")
    print(f"  Yüksek risk:    {high}")
    print(f"  Orta risk:      {medium}")
    print(f"  Düşük risk:     {low}")
    print(f"  Hata:           {errors}")

# ---------- URL listesi okuma ----------

def load_urls(filename):
    """Dosyadan URL listesi okur (her satır bir URL, # ile başlayanlar yorum)."""
    urls = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls

# ---------- Ana akış ----------

def main():
    print("=" * 60)
    print("HTTP SECURITY HEADER SCANNER")
    print("=" * 60)

    print("\n  1) Dosyadan URL listesi yükle (urls.txt)")
    print("  2) Manuel URL gir")
    secim = input("\nSeçim: ").strip()

    if secim == "1":
        try:
            urls = load_urls("urls.txt")
            print(f"\n[+] {len(urls)} URL yüklendi.")
        except FileNotFoundError:
            print("[!] urls.txt bulunamadı. Manuel girişe geçiliyor.")
            urls = [input("URL: ").strip()]
    else:
        urls = [input("URL: ").strip()]

    results = []
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Taranıyor: {url}")
        result = scan_url(url)
        print_result(result)
        results.append(result)

    print_summary(results)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(results, f"scan_{timestamp}.json")
    save_csv(results, f"scan_{timestamp}.csv")

if __name__ == "__main__":
    main()
