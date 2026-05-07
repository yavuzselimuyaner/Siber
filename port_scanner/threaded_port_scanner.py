from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import socket


def grab_banner(ip, port, timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))

        if port in (80, 8080, 8000):
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")

        banner = sock.recv(1024).decode(errors="ignore").strip()
        sock.close()
        return banner.split("\n")[0] if banner else "No banner"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return "No banner"
    except Exception as e:
        return f"Error: {str(e)}"


def scan_port(ip, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            banner = grab_banner(ip, port)
            return (port, True, banner)
        return (port, False, "")
    except Exception:
        return (port, False, "")


def scan_single_thread(ip, ports):
    results = []
    for port in ports:
        p, is_open, banner = scan_port(ip, port)
        if is_open:
            results.append((p, banner))
    return results


def scan_multi_thread(ip, ports, max_workers=100):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in ports}
        for future in as_completed(futures):
            p, is_open, banner = future.result()
            if is_open:
                results.append((p, banner))
    return sorted(results)


def print_results(results):
    if not results:
        print("  Açık port bulunamadı.")
        return
    for port, banner in sorted(results):
        print(f"  [OPEN] {port}/tcp → {banner}")


def show_menu():
    print("\n" + "=" * 50)
    print("PORT TARAYICI v2 (Multi-Thread)")
    print("=" * 50)
    print("  1) Tek thread tarama (yavaş)")
    print("  2) Multi-thread tarama (hızlı)")
    print("  3) Her ikisini de çalıştır ve karşılaştır")
    print("  0) Çıkış")
    print("=" * 50)


if __name__ == "__main__":
    target = "scanme.nmap.org"
    ports = list(range(1, 1025))

    try:
        ip = socket.gethostbyname(target)
        print(f"Hedef: {target} ({ip})")
        print(f"Taranan port sayısı: {len(ports)}")
    except socket.gaierror:
        print(f"Hedef çözümlenemedi: {target}")
        exit(1)

    while True:
        show_menu()
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            print("\n" + "=" * 50)
            print("TEK THREAD TARAMA")
            print("=" * 50)
            start = time.time()
            results = scan_single_thread(ip, ports)
            elapsed = time.time() - start
            print_results(results)
            print(f"\nSüre: {elapsed:.2f} saniye")

        elif secim == "2":
            print("\n" + "=" * 50)
            print("MULTI-THREAD TARAMA (100 worker)")
            print("=" * 50)
            start = time.time()
            results = scan_multi_thread(ip, ports, max_workers=100)
            elapsed = time.time() - start
            print_results(results)
            print(f"\nSüre: {elapsed:.2f} saniye")

        elif secim == "3":
            print("\n" + "=" * 50)
            print("TEK THREAD TARAMA")
            print("=" * 50)
            start = time.time()
            single_results = scan_single_thread(ip, ports)
            single_time = time.time() - start
            print_results(single_results)
            print(f"\nSüre: {single_time:.2f} saniye")

            print("\n" + "=" * 50)
            print("MULTI-THREAD TARAMA (100 worker)")
            print("=" * 50)
            start = time.time()
            multi_results = scan_multi_thread(ip, ports, max_workers=100)
            multi_time = time.time() - start
            print_results(multi_results)
            print(f"\nSüre: {multi_time:.2f} saniye")

            print("\n" + "=" * 50)
            print("KARŞILAŞTIRMA")
            print("=" * 50)
            speedup = single_time / multi_time if multi_time > 0 else 0
            print(f"Tek thread:   {single_time:.2f}s")
            print(f"Multi thread: {multi_time:.2f}s")
            print(f"Hızlanma:     {speedup:.2f}x")

        elif secim == "0":
            print("Çıkılıyor...")
            break

        else:
            print("Geçersiz seçim, tekrar deneyin.")
