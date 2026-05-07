import argparse
import json
import socket

parser = argparse.ArgumentParser(description="Basit TCP port tarayıcı")
parser.add_argument("--host", required=True, help="Hedef host veya IP")
parser.add_argument("--start", type=int, required=True, help="Başlangıç portu")
parser.add_argument("--end", type=int, required=True, help="Bitiş portu")
args = parser.parse_args()

print(f"Host: {args.host}")
print(f"Port aralığı: {args.start} - {args.end}")

open_ports = {}
print(f"[*] Tarama başlatıldı: {args.host} taraniyor {args.start} - {args.end} portları arasında...")

for port in range(args.start, args.end + 1):
    print(f"Taranıyor: {port}", end='\r', flush=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((args.host, port))
    if result == 0:
        open_ports[port] = "Açık"
    sock.close()

with open("results.json", "w") as f:
    json.dump(open_ports, f, indent=4)

print(f"\n[*] Tarama tamamlandı. Açık portlar results.json dosyasına kaydedildi.")
