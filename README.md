# Siber Güvenlik — Araçlar, Writeup'lar, Notlar

Eğitim amaçlı geliştirilen Python tabanlı siber güvenlik araçları, HackTheBox / PortSwigger / picoCTF pratiklerinin writeup'ları ve pentest sırasında biriken hızlı başvuru notları.

> **Uyarı:** Tüm araçlar yalnızca yetkili sistemlerde ve eğitim ortamlarında kullanılmalıdır.

---

## Proje Yapısı

```
Siber/
├── http_header_scanner/
│   └── http_header_scanner.py   # HTTP güvenlik header analizi
├── port_scanner/
│   ├── port_scanner.py          # Temel TCP port tarayıcı
│   └── threaded_port_scanner.py # Multi-thread port tarayıcı + banner grabbing
├── subdomain_scanner/
│   └── subdomain_scanner.py     # DNS tabanlı subdomain keşfi
├── socket_basics/
│   ├── banner_grabber.py        # Raw socket & banner grabbing demo
│   └── banner_analysis.md       # Örnek banner grabbing analiz raporu
├── writeups/
│   ├── htb/                     # HackTheBox makine writeup'ları + TEMPLATE
│   └── portswigger/             # OWASP Top 10 lab writeup'ları + TEMPLATE
├── picoCTF/                     # picoCTF challenge çözümleri
└── notes/
    ├── owasp-top10-quickref.md  # OWASP Top 10 hızlı referans
    ├── linux-privesc-checklist.md
    ├── nmap-reference.md
    ├── burp-workflow.md
    └── reverse-shells.md
```

---

## Araçlar

### 1. HTTP Güvenlik Header Tarayıcı

Web sitelerinin HTTP başlıklarını analiz eder, eksik güvenlik başlıklarını ve bilgi sızdıran başlıkları tespit eder.

**Kontrol ettiği başlıklar:**
- `Content-Security-Policy`, `X-Frame-Options` — eksikse risk
- `Server`, `X-Powered-By` — varsa bilgi sızıntısı

```bash
pip install requests
cd http_header_scanner
python http_header_scanner.py
```

---

### 2. Temel Port Tarayıcı

Komut satırı argümanlarıyla belirtilen host ve port aralığını tarar.

```bash
cd port_scanner
python port_scanner.py --host scanme.nmap.org --start 1 --end 1024
```

---

### 3. Multi-Thread Port Tarayıcı

Tek thread ve multi-thread modlarını karşılaştırmalı sunar; açık portlardan banner bilgisi çeker.

```bash
cd port_scanner
python threaded_port_scanner.py
```

---

### 4. Subdomain Tarayıcı

Wordlist kullanarak DNS çözümlemesiyle alt domainleri keşfeder.

```bash
# Wordlist indir:
# https://github.com/danielmiessler/SecLists/raw/master/Discovery/DNS/subdomains-top1million-5000.txt
# İndirilen dosyayı wordlist.txt olarak kaydet

cd subdomain_scanner
python subdomain_scanner.py
```

---

### 5. Socket Temelleri & Banner Grabbing

Temel Python socket kullanımını gösteren, birden fazla hedefe bağlanarak banner bilgisi çeken demo.

```bash
cd socket_basics
python banner_grabber.py
```

Analiz raporu: [`socket_basics/banner_analysis.md`](socket_basics/banner_analysis.md)

---

## Kurulum

```bash
git clone https://github.com/<kullanici-adin>/Siber.git
cd Siber
pip install requests
```

---

## Writeup'lar & Pratik

- **HackTheBox** — [`writeups/htb/`](writeups/htb/) (recon → exploit → priv-esc döngüsü)
- **PortSwigger Web Security Academy** — [`writeups/portswigger/`](writeups/portswigger/) (OWASP Top 10 lab'leri)
- **picoCTF** — [`picoCTF/`](picoCTF/) (cripto, web, forensics, binary)

## Notlar

[`notes/`](notes/) altında pentest sırasında sık başvurulan cheatsheet'ler:

- OWASP Top 10 hızlı referans
- Linux yetki yükseltme kontrol listesi
- Nmap bayrak referansı
- Burp Suite iş akışı
- Reverse shell tek satırlık komutlar

## Öğrenilen Konular

| Konu | Klasör |
|------|--------|
| HTTP header analizi & risk skorlama | `http_header_scanner/` |
| TCP soket bağlantısı & port tarama | `port_scanner/port_scanner.py` |
| ThreadPoolExecutor & eşzamanlılık | `port_scanner/threaded_port_scanner.py` |
| DNS çözümleme & subdomain keşfi | `subdomain_scanner/` |
| Raw socket & banner grabbing | `socket_basics/` |
| Web zafiyet exploitation (OWASP Top 10) | `writeups/portswigger/` |
| Penetrasyon testi metodolojisi | `writeups/htb/` |
