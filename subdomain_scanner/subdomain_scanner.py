import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


def load_wordlist(path):
    with open(path, "r") as f:
        words = [line.strip() for line in f if line.strip()]
    return words


def check_subdomain(subdomain, domain):
    full_domain = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return (full_domain, ip)
    except socket.gaierror:
        return None


def scan(domain, wordlist, max_threads=50):
    """Wordlist'teki subdomainleri paralel olarak kontrol et."""
    found = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {
            executor.submit(check_subdomain, word, domain): word
            for word in wordlist
        }

        for i, future in enumerate(as_completed(futures), start=1):
            result = future.result()
            if result:
                full_domain, ip = result
                print(f"[+] BULUNDU: {full_domain} → {ip}")
                found.append(result)

            if i % 500 == 0:
                print(f"    ... {i}/{len(wordlist)} kontrol edildi")

    return found


def save_results(found, output_path):
    """Bulunan subdomainleri dosyaya yaz."""
    with open(output_path, "w") as f:
        for full_domain, ip in found:
            f.write(f"{full_domain} {ip}\n")
    print(f"[*] Sonuçlar '{output_path}' dosyasına kaydedildi")


if __name__ == "__main__":
    domain = "hackerone.com"
    wordlist_path = "wordlist.txt"  # subdomains-top1million-5000.txt gibi bir wordlist

    wordlist = load_wordlist(wordlist_path)

    print(f"[*] Hedef: {domain}")
    print(f"[*] {len(wordlist)} subdomain denenecek\n")

    found = scan(domain, wordlist, max_threads=50)

    print(f"\n[*] Toplam {len(found)} subdomain bulundu")
    if found:
        save_results(found, "found_subdomains.txt")
