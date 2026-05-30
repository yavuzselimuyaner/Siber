# Burp Suite — İş Akışı Notları

## Kurulum Kontrolü

- Browser proxy: `127.0.0.1:8080`
- Burp CA cert: tarayıcıya kurulu mu? (HTTPS interception)
- Target → Scope: hedef domain'i scope'a al, "Show only in-scope items" aç.

## Modüller — Ne Zaman Hangisi

| Modül | Kullanım |
|-------|----------|
| **Proxy** | Trafik yakala, intercept aç/kapat |
| **HTTP History** | Geçmiş istekleri tara, ilginç olanı Repeater'a yolla |
| **Repeater** | Tek isteği elle manipüle et, payload dene |
| **Intruder** | Otomatik fuzz (parametre, header, path) — Community'de yavaş ama yine işe yarar |
| **Decoder** | URL/Base64/Hex/HTML encode-decode |
| **Comparer** | İki response'u diff'le (Sniper attack sonucu önemli) |
| **Sequencer** | Token rastgeleliği |

## Tipik Akış

1. **Browse** — Manuel olarak uygulamayı kullan, tüm endpoint'ler History'ye düşsün.
2. **Map** — Target → Site map içinde dizin ağacını gör; eksik endpoint'leri gobuster ile tamamla.
3. **Triage** — Login, file upload, search, admin, API endpoint'lerini işaretle.
4. **Repeat & Tamper** — Repeater'da:
   - Parametre değerlerini değiştir (boolean, integer, string)
   - Header ekle/çıkar (`X-Forwarded-For`, `Host`, `Origin`)
   - Method değiştir (GET ↔ POST, OPTIONS, PUT)
5. **Intruder Patterns:**
   - **Sniper**: tek pozisyon, tek liste
   - **Battering ram**: tüm pozisyonlara aynı payload
   - **Pitchfork**: paralel listeler (username + password)
   - **Cluster bomb**: kartezyen çarpım (brute force)

## Hızlı Test Şablonu

### Auth Bypass

```http
GET /admin HTTP/1.1
X-Forwarded-For: 127.0.0.1
X-Original-URL: /admin
X-Rewrite-URL: /admin
```

### SQLi Hızlı Sweep

Intruder payload'u: `SecLists/Fuzzing/SQLi/Generic-SQLi.txt`

### Path Traversal

```
../../../etc/passwd
....//....//....//etc/passwd
%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

## Kısayollar

- `Ctrl+R` — Repeater'a yolla
- `Ctrl+I` — Intruder'a yolla
- `Ctrl+U` — URL encode seçili text
- `Ctrl+Shift+U` — URL decode
