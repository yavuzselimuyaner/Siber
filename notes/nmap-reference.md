# Nmap — Hızlı Referans

## Temel Tarama Tipleri

| Bayrak | Anlam |
|--------|-------|
| `-sS` | TCP SYN (stealth, default root) |
| `-sT` | TCP connect (root değilse) |
| `-sU` | UDP (yavaş ama kritik) |
| `-sV` | Servis sürüm tespiti |
| `-sC` | Default NSE script'leri |
| `-O` | OS tespiti |
| `-A` | -sV -sC -O --traceroute hepsi bir arada |
| `-Pn` | Ping atma (ICMP filtreli ortamlar) |
| `-n` | DNS çözmeyi atla (hız) |

## Port Seçimi

```bash
-p 22,80,443           # belirli portlar
-p-                    # tüm 65535
-p 1-1000              # aralık
--top-ports 1000       # en yaygın 1000
-F                     # fast scan (top 100)
```

## Hız / Stealth

```bash
-T0 ... -T5            # 0 paranoid, 5 insane
--min-rate 1000        # paket/sn alt sınırı
--max-retries 1
```

## Çıktı

```bash
-oN out.txt            # normal
-oG out.grep           # greppable
-oX out.xml            # XML (parsable)
-oA basename           # 3'ü birden
```

## Kullanışlı Hazır Reçeteler

```bash
# Hızlı initial recon
nmap -sC -sV -oN nmap/initial.txt <IP>

# Tüm portlar
nmap -p- --min-rate 5000 -oN nmap/all-ports.txt <IP>

# UDP top 100
sudo nmap -sU --top-ports 100 -oN nmap/udp.txt <IP>

# Belirli portlar derin tarama
nmap -sC -sV -p 22,80,443 -A -oN nmap/deep.txt <IP>

# Vuln script'leri
nmap --script vuln -p 80,443 <IP>

# SMB enum
nmap --script smb-enum-shares,smb-enum-users -p 445 <IP>

# HTTP enum
nmap --script http-enum,http-title,http-headers -p 80,443 <IP>
```

## NSE Kategorileri

`auth`, `broadcast`, `brute`, `default`, `discovery`, `dos`, `exploit`, `external`, `fuzzer`, `intrusive`, `malware`, `safe`, `version`, `vuln`

```bash
nmap --script "default and safe" <IP>
nmap --script "smb-vuln-*" -p 445 <IP>
```
