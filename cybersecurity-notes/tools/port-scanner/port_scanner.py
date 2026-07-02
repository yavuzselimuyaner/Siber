import argparse
import json
import socket

parser = argparse.ArgumentParser(description="Simple TCP port scanner")
parser.add_argument("--host", required=True, help="Target host or IP")
parser.add_argument("--start", type=int, required=True, help="Starting port")
parser.add_argument("--end", type=int, required=True, help="Ending port")
args = parser.parse_args()

print(f"Host: {args.host}")
print(f"Port range: {args.start} - {args.end}")

open_ports = {}
print(f"[*] Scanning started: {args.host} on ports {args.start} - {args.end}...")

for port in range(args.start, args.end + 1):
    print(f"Scanning: {port}", end='\r', flush=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((args.host, port))
    if result == 0:
        open_ports[port] = "Open"
    sock.close()

with open("results.json", "w") as f:
    json.dump(open_ports, f, indent=4)

print(f"\n[*] Scan completed. Open ports saved to results.json")
