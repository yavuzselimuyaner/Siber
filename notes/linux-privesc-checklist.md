# Linux Privilege Escalation — Kontrol Listesi

İlk shell'i aldıktan sonra sırayla bak.

## 1. Bilgi Toplama

```bash
id
whoami
hostname
uname -a
cat /etc/os-release
cat /etc/passwd | grep -v nologin
ps auxf
ss -tulnp
netstat -tulnp
```

## 2. Sudo

```bash
sudo -l                       # nopasswd?
sudo -V                       # CVE-2021-3156 etc.
```

GTFOBins kontrol: https://gtfobins.github.io/

## 3. SUID / SGID

```bash
find / -perm -4000 -type f 2>/dev/null
find / -perm -2000 -type f 2>/dev/null
```

Sıradışı bir SUID binary varsa → GTFOBins.

## 4. Capabilities

```bash
getcap -r / 2>/dev/null
```

`cap_setuid`, `cap_sys_admin`, `cap_dac_read_search` → tehlikeli.

## 5. Cron

```bash
cat /etc/crontab
ls -la /etc/cron.*
crontab -l
```

Yazılabilir script + root cron = win.

## 6. Yazılabilir Dosya/Dizin

```bash
find / -writable -type f 2>/dev/null | grep -v proc
find / -perm -o+w -type d 2>/dev/null
```

## 7. PATH Hijacking

```bash
echo $PATH
```

`.` PATH'te varsa veya yazılabilir dizin başta ise → sahte binary.

## 8. Kernel Exploit

```bash
uname -r
searchsploit linux kernel <version>
```

Son çare. Stabiliteyi bozar.

## 9. Otomatik Araçlar

- [linpeas.sh](https://github.com/carlospolop/PEASS-ng)
- [LinEnum.sh](https://github.com/rebootuser/LinEnum)
- [pspy](https://github.com/DominicBreuker/pspy) — root cron canlı izleme

## 10. Sık Kaçırılan

- `.bash_history`, `.viminfo`, `.gitconfig` içinde credential
- `/var/backups/`, `/opt/`, `/tmp/`, `/root/` (okunabiliyorsa)
- MySQL/PostgreSQL boş şifre
- Docker grubunda olmak → root
- `LD_PRELOAD`, `LD_LIBRARY_PATH` env keep
