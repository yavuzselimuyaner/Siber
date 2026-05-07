import socket
import sys


targets = [
    ('www.google.com', 80),
    ('bandit.labs.overthewire.org', 22),
    ('ftp.dlptest.com', 21),
    ('smtp.gmail.com', 25),
]

for host, port in targets:
    try:
        host_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] Host çözümlenemedi: {host}")
        sys.exit()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[+] Socket oluşturuldu")
    except socket.error as err:
        print(f"[!] Socket oluşturulamadı: {err}")

    try:
        s.settimeout(2)
        s.connect((host_ip, port))
        print(f"[+] {host}:{port} bağlantısı başarılı")

        if port == 80:
            s.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")

        data = s.recv(1024)
        with open("banner_report.txt", "a") as f:
            f.write(f"=== {host}:{port} ===\n")
            f.write(data.decode('utf-8', errors='ignore'))
            f.write("\n\n")

        print(f"[*] {host}:{port} banner:\n{data.decode('utf-8', errors='ignore')[:200]}")

    except socket.error as err:
        print(f"[!] {host}:{port} bağlantı hatası: {err}")
    finally:
        s.close()
