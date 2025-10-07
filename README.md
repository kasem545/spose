# Spose
**Squid Pivoting Open Port Scanner**  
> Threaded scanner with banner grabbing over HTTP CONNECT tunnels

Detect open ports on internal hosts *through a Squid HTTP proxy*. Useful for **CTF**, **red team**, and **pentesting** scenarios where you can pivot via an HTTP proxy.

---

## ✨ Features

- 🔀 Multi-threaded scanning (`--threads`)
- 🕵️‍♂️ Port **banner grabbing** (via HTTP `HEAD` requests)
- 🎯 Accurate results – avoids false positives from generic proxy responses
- ⚡ Optional full 65,535 port scan
- 💥 Designed for use in **proxy pivoting** scenarios (like Squid / Burp)

---

## 🚀 Usage

```bash
❯ python3 ./spose.py --help
usage: spose.py [-h] --proxy PROXY --target TARGET [--ports PORTS] [--allports] [--threads THREADS]

Squid Proxy Port Scanner with Threading and Banner Grabbing

options:
  -h, --help         Show help message and exit
  --proxy PROXY      Proxy address URL (e.g. http://127.0.0.1:3128)
  --target TARGET    Internal target IP behind the proxy
  --ports PORTS      [Optional] Comma-separated list of ports (e.g. 22,80,443)
  --allports         [Optional] Scan all 65,535 TCP ports
  --threads THREADS  [Optional] Number of concurrent threads (default: 50)
```

### 🔧 Examples

Scan common ports:
```bash
python3 spose.py --proxy http://127.0.0.1:3128 --target 10.10.1.5
```

Scan specific ports with 100 threads:
```bash
python3 spose.py --proxy http://127.0.0.1:3128 --target 10.10.1.5 --ports 21,22,80,443 --threads 100
```

Full port scan:
```bash
python3 spose.py --proxy http://127.0.0.1:3128 --target 10.10.1.5 --allports --threads 300
```

---

## 📦 Tested On

- ✅ `sickOS 1.1` (VulnHub)
- ✅ `pinkys-palace` (VulnHub)

---

## 🔗 References

- [Rapid7 - Squid Proxy Port Scanning](https://www.rapid7.com/db/modules/auxiliary/scanner/http/squid_pivot_scanning)

---
## 🙏 Credit

- Originally created by [aancw](https://github.com/aancw/spose)

---

## 📄 License

MIT License — do whatever you want, just don’t blame me.

---

> 🧠 Tip: Some proxies block low ports or restrict `CONNECT` to a whitelist. Test with `curl -x` to verify:
> ```bash
> curl -x http://127.0.0.1:3128 http://10.10.1.5:80
> ```
