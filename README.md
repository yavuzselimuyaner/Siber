# Banner Grabbing Raporu

## Genel Bilgi

Bu rapor, hedef sistemlere yönelik gerçekleştirilen banner grabbing (afiş yakalama) tekniğiyle elde edilen servis bilgilerini içermektedir. Amaç; açık portlarda çalışan servislerin sürüm ve yapılandırma bilgilerini pasif olarak tespit etmektir.

---

## Tespit Edilen Servisler

### 1. HTTP Servisi

| Alan | Değer |
|------|-------|
| Protokol | HTTP/1.1 |
| Durum Kodu | 200 OK |
| Sunucu | gws (Google Web Server) |
| Content-Type | text/html; charset=ISO-8859-1 |
| X-Frame-Options | SAMEORIGIN |
| X-XSS-Protection | 0 |

#### HTTP Başlık Analizi

**Content-Security-Policy-Report-Only**
- CSP yalnızca `report-only` modunda tanımlı; ihlaller engellenmez, sadece raporlanır.
- `unsafe-eval` ve `unsafe-inline` direktifleri izin verilen kaynaklar arasında yer almaktadır.

**X-XSS-Protection: 0**
- Tarayıcı tabanlı XSS filtresi devre dışı bırakılmış. Modern yaklaşımda CSP bu rolü üstlenir.

**X-Frame-Options: SAMEORIGIN**
- Sayfa yalnızca aynı kaynaktan (origin) iframe içinde yüklenebilir. Clickjacking saldırılarına karşı koruma sağlar.

**Set-Cookie Başlıkları**

| Cookie | Güvenlik Bayrakları | Notlar |
|--------|---------------------|--------|
| `__Secure-STRP` | `Secure`, `SameSite=strict` | Kısa süreli oturum çerezi (5 dakika) |
| `AEC` | `Secure`, `HttpOnly`, `SameSite=lax` | 6 aylık süre, JS erişimi yok |
| `NID` | — | Tercih/oturum çerezi |

---

### 2. SSH Servisi

```
Banner: SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.15
```

| Alan | Değer |
|------|-------|
| Protokol | SSH-2.0 |
| Yazılım | OpenSSH 9.6p1 |
| İşletim Sistemi | Ubuntu (3ubuntu13.15) |

**Bulgular:**
- Sunucunun Ubuntu tabanlı bir Linux sistemi olduğu ve OpenSSH 9.6p1 çalıştırdığı tespit edilmiştir.
- Bu bilgi hedef sistem hakkında OS fingerprinting için kullanılabilir.

---

### 3. FTP Servisi

```
220 Welcome to the DLP Test FTP Server
```

| Alan | Değer |
|------|-------|
| Port | 21 (FTP) |
| Banner | Welcome to the DLP Test FTP Server |

**Bulgular:**
- FTP servisi aktif ve banner bilgisi açık şekilde yayınlanmaktadır.
- "DLP Test" ifadesi bu sunucunun bir test/lab ortamına ait olduğuna işaret etmektedir.
- FTP şifrelenmemiş bir protokoldür; kimlik bilgileri ve veri açık metin olarak iletilir.

---

## Güvenlik Değerlendirmesi

| Bulgu | Risk | Öneri |
|-------|------|-------|
| SSH sürüm bilgisi açıkta | Düşük | `VersionAddendum` ile banner gizlenebilir |
| FTP servisi aktif (şifresiz) | Yüksek | SFTP veya FTPS ile değiştirilmeli |
| CSP `report-only` modunda | Orta | Enforce moduna geçirilmeli |
| `NID` çerezinde `Secure`/`HttpOnly` bayrağı yok | Düşük | Bayraklar eklenmeli |

---

## Araç ve Yöntem

Aşağıdaki araçlarla banner grabbing gerçekleştirilebilir:

```bash
# HTTP banner
curl -I http://<hedef>

# FTP banner
nc <hedef> 21

# SSH banner
nc <hedef> 22

# Nmap ile tüm servisler
nmap -sV --script=banner <hedef>
```

---

## Notlar

- Bu rapor yalnızca eğitim ve yetkilendirilmiş test amaçlıdır.
- Tarih: 23 Nisan 2026
