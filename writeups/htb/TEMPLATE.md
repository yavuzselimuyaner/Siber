# {MAKİNE_ADI}

| Alan | Değer |
|------|-------|
| Platform | HackTheBox |
| Zorluk | Easy / Medium / Hard |
| OS | Linux / Windows |
| Tarih | YYYY-MM-DD |
| Tag'ler | web, lfi, sqli, kernel-exploit ... |

## Özet

> Tek paragrafta exploit zinciri: ilk erişim → user → root.

---

## 1. Recon

### Nmap

```bash
nmap -sC -sV -oN nmap/initial.txt <IP>
```

```
# çıktı
```

**Tespitler:**
- Port X: servis Y, sürüm Z → ...

### Web Keşfi

```bash
gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt
whatweb http://<IP>
```

---

## 2. Enumeration

> Hangi servisi neden derinleştirdin? Nereye kanca attın?

---

## 3. Initial Foothold

### Zafiyet

- CVE / OWASP kategorisi
- Etkilenen bileşen
- Tetikleyici parametre / endpoint

### Payload

```http
POST /endpoint HTTP/1.1
...
```

### Shell

```bash
# reverse shell komutu
```

---

## 4. User → Root

### Lateral Movement (varsa)

### Privilege Escalation

```bash
# linpeas / sudo -l / SUID / cron / capabilities bulguları
```

**Kullanılan vektör:** ...

---

## 5. Flags

- `user.txt`: ✓
- `root.txt`: ✓

---

## 6. Lessons Learned

- ...
- ...

## 7. Defansif Bakış

> Bu makineyi sertleştirmek için ne yapılmalıydı? (config, patch, least privilege ...)
