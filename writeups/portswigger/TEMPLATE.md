# {LAB_ADI}

| Alan | Değer |
|------|-------|
| Konu | SQLi / XSS / SSRF / CSRF / Access Control / ... |
| OWASP | A0X — Kategori |
| Zorluk | Apprentice / Practitioner / Expert |
| Tarih | YYYY-MM-DD |

## Açıklama

> PortSwigger lab açıklamasının kısa özeti.

---

## Recon

- Hedef endpoint
- Parametre haritası
- Gözlenen davranış / hata mesajı

---

## Zafiyetin Tespiti

> Hangi anormalliği gördün? Niye bu sınıfa girdiğine karar verdin?

---

## Exploit

### Payload

```
{ZARARLI_İSTEK}
```

### Burp Request

```http
POST /endpoint HTTP/1.1
Host: ...
Cookie: session=...

param=PAYLOAD
```

### Sonuç

> Lab "solved" oldu mu? Hangi bilgiyi sızdırdın / hangi aksiyonu tetikledin?

---

## Defansif Karşılık

> Geliştirici ne yapsaydı bu zafiyet olmazdı? (parametrize sorgu, CSP, SameSite cookie, allow-list, vb.)

## Notlar

- ...
